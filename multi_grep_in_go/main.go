package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"io/fs"
	"io/ioutil"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
)

func checkError(err error) {
	if err != nil {
		panic(err)
	}
}

func Walk(dirPath string, fileChan chan string) {
	err := filepath.Walk(dirPath, func(fPath string, info fs.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}
		fileSuffix := path.Ext(fPath)
		if strings.ToLower(fileSuffix) == ".md" {
			fileChan <- fPath
		}
		return nil
	})
	checkError(err)
	close(fileChan)
}

func _filter(wg *sync.WaitGroup, syncChan chan struct{}, targetChan chan string, filePath string, keywords []string) {
	defer func() {
		wg.Done()
		<-syncChan
	}()

	content, err := ioutil.ReadFile(filePath)
	checkError(err)
	if !argCaseSensitive {
		content = bytes.ToLower(content)
	}

	for _, ele := range keywords {
		if !bytes.Contains(content, []byte(ele)) {
			return
		}
	}
	found = append(found, filePath)
	targetChan <- filePath
}

func filter(fileChan chan string, syncChan chan struct{}, targetChan chan string, keywords []string) {
	var wg sync.WaitGroup
	for file := range fileChan {
		wg.Add(1)
		syncChan <- struct{}{}
		go _filter(&wg, syncChan, targetChan, file, keywords)
	}
	wg.Wait()
	close(targetChan)
}

func printResult(targetChan chan string, endChan chan struct{}) {
	idx := 0
	for ele := range targetChan {
		fmt.Printf("%3s  %s\n", strconv.Itoa(idx), ele)
		idx++
	}
	endChan <- struct{}{}
}

func execWinShell(name string, arg ...string) error {
	command := append([]string{"/C", name}, arg...)
	cmd := exec.Command("cmd", command...)
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		return err
	}
	fmt.Printf("%s", out.String())
	return nil
}

func getIndexes() []int {
	fmt.Println("\n请选择要打开文件的序号, 以空格做分隔(不填则打开全部文件):")
	reader := bufio.NewReader(os.Stdin)
	content, err := reader.ReadString('\n')
	checkError(err)

	var indexList []int
	content = strings.TrimSpace(content)
	temp := strings.Split(content, " ")
	for _, ele := range temp {
		if len(ele) == 0 {
			continue
		}
		if num, err := strconv.Atoi(ele); err == nil {
			indexList = append(indexList, num)
		}
	}
	return indexList
}

func getFiles(indexes []int) []string {
	if len(indexes) == 0 {
		return found
	}

	var files []string
	for _, idx := range indexes {
		if 0 <= idx && idx <= len(found)-1 {
			files = append(files, found[idx])
		}
	}

	return files
}

func openFile(editor string, files []string) {
	if len(files) == 0 {
		fmt.Println("error: len(files)==0")
		return
	}

	err := execWinShell(editor, files...)
	checkError(err)
}

const (
	defaultDirPath = "D:\\myshare\\Dropbox\\root\\md"
	defaultEditor  = "code"
)

var (
	argDirPath       string
	argEditor        string
	argCaseSensitive bool
	argKeywords      []string

	found []string
)

func parseArg() {
	flag.StringVar(&argDirPath, "p", defaultDirPath, "search dir")
	flag.StringVar(&argEditor, "e", defaultEditor, "editor")
	flag.BoolVar(&argCaseSensitive, "c", false, "case sensitive")
	flag.Parse()

	argKeywords = flag.Args()
	argDirPath = strings.TrimSpace(argDirPath)
	argEditor = strings.TrimSpace(argEditor)
	if !argCaseSensitive {
		for idx, keyword := range argKeywords {
			argKeywords[idx] = strings.ToLower(keyword)
		}
	}
}

func main() {
	parseArg()
	if len(argKeywords) == 0 {
		fmt.Println("error: len(keywords)==0")
		return
	}

	fmt.Println()

	fileChan := make(chan string, 1024)
	targetChan := make(chan string, 1024)
	syncChan := make(chan struct{}, 20)
	endChan := make(chan struct{}, 1)

	go printResult(targetChan, endChan)
	go filter(fileChan, syncChan, targetChan, argKeywords)
	go Walk(argDirPath, fileChan)
	<-endChan

	indexes := getIndexes()
	files := getFiles(indexes)
	openFile(argEditor, files)
}
