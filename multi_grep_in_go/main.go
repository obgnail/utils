package main

import (
	"bufio"
	"bytes"
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

func toLower(keywords []string) {
	for idx, value := range keywords {
		keywords[idx] = strings.ToLower(value)
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
	content = bytes.ToLower(content)

	for _, ele := range keywords {
		if !bytes.Contains(content, []byte(ele)) {
			return
		}
	}
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

func printResult(targetChan chan string, toSearch *[]string, endChan chan struct{}) {
	idx := 0
	for ele := range targetChan {
		fmt.Printf("%3s  %s\n", strconv.Itoa(idx), ele)
		*toSearch = append(*toSearch, ele)
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

func getFiles(toSearch []string, indexes []int) []string {
	if len(indexes) == 0 {
		return toSearch
	}

	var files []string
	for _, idx := range indexes {
		if idx > len(toSearch)-1 || idx < 0 {
			continue
		}
		files = append(files, toSearch[idx])
	}

	return files
}

func openInVSCode(files []string) {
	if len(files) == 0 {
		fmt.Println("error: len(files)==0")
		return
	}

	err := execWinShell("code", files...)
	checkError(err)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("error: len(os.Args)<2")
		return
	}

	fmt.Println()

	dirPath := "D:\\myshare\\Dropbox\\root\\md"
	keywords := os.Args[1:]

	var toSearch []string
	fileChan := make(chan string, 1024)
	targetChan := make(chan string, 1024)
	syncChan := make(chan struct{}, 20)
	endChan := make(chan struct{}, 1)

	toLower(keywords)
	go printResult(targetChan, &toSearch, endChan)
	go filter(fileChan, syncChan, targetChan, keywords)
	go Walk(dirPath, fileChan)
	<-endChan

	indexes := getIndexes()
	files := getFiles(toSearch, indexes)
	openInVSCode(files)
}
