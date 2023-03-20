package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
)

func main() {
	args := os.Args
	if args[1] != "get" {
		fmt.Println("support \"get\" only")
		return
	}

	packagePath := args[2]
	paths := strings.Split(packagePath, "/")

	if len(paths) != 3 {
		fmt.Println("package path error")
		return
	}
	if paths[0] != "github.com" {
		fmt.Println("support github.com only")
		return
	}

	goPath := os.Getenv("GOPATH")
	target := filepath.Join(goPath, "src", "github.com", paths[1], paths[2])

	command := fmt.Sprintf("git clone -- git@github.com:%s/%s.git %s", paths[1], paths[2], target)

	fmt.Println(command)

	cmd := exec.Command("cmd", "/C", command)
	PrintCmdOutput(cmd)
}

func PrintCmdOutput(cmd *exec.Cmd) {
	cmd.Stdin = os.Stdin

	var wg sync.WaitGroup
	wg.Add(2)
	//捕获标准输出
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("INFO:", err)
		os.Exit(1)
	}
	readout := bufio.NewReader(stdout)
	go func() {
		defer wg.Done()
		GetOutput(readout)
	}()

	//捕获标准错误
	stderr, err := cmd.StderrPipe()
	if err != nil {
		fmt.Println("ERROR:", err)
		os.Exit(1)
	}
	readerr := bufio.NewReader(stderr)
	go func() {
		defer wg.Done()
		GetOutput(readerr)
	}()

	//执行命令
	err = cmd.Run()
	if err != nil {
		return
	}
	wg.Wait()
}

func GetOutput(reader *bufio.Reader) {
	var sumOutput string //统计屏幕的全部输出内容
	outputBytes := make([]byte, 200)
	for {
		n, err := reader.Read(outputBytes) //获取屏幕的实时输出(并不是按照回车分割，所以要结合sumOutput)
		if err != nil {
			if err == io.EOF {
				break
			}
			fmt.Println(err)
			sumOutput += err.Error()
		}
		output := string(outputBytes[:n])
		fmt.Print(output) //输出屏幕内容
		sumOutput += output
	}
}
