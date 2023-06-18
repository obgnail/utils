package main

import (
	"bytes"
	"fmt"
	"io/fs"
	"io/ioutil"
	"os"
	"path"
	"path/filepath"
	"strings"
	"sync"
)

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
	if err != nil {
		panic(err)
	}
	close(fileChan)
}

func _filter(wg *sync.WaitGroup, syncChan chan struct{}, targetChan chan string, filePath string, keywords []string) {
	defer func() {
		wg.Done()
		<-syncChan
	}()

	content, err := ioutil.ReadFile(filePath)
	if err != nil {
		panic(err)
	}
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

func printResult(targetChan chan string, exitChan chan struct{}) {
	for ele := range targetChan {
		fmt.Println(ele)
	}
	exitChan <- struct{}{}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("error: os.args length must > 1")
		return
	}

	dirPath := "D:\\myshare\\Dropbox\\root\\md"
	keywords := os.Args[1:]

	fileChan := make(chan string, 1024)
	targetChan := make(chan string, 1024)
	syncChan := make(chan struct{}, 20)
	exitChan := make(chan struct{}, 1)

	toLower(keywords)
	go printResult(targetChan, exitChan)
	go filter(fileChan, syncChan, targetChan, keywords)
	go Walk(dirPath, fileChan)
	<-exitChan
}
