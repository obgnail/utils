package main

import (
	"bytes"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path"
	"strings"
)

const (
	dockerGOPATH    = "/go"
	myGOPATH        = "/d/golang"
	dockerGoTag     = "golang:1.18"
	startFlagInPath = "golang"
)

func main() {
	var escapeBackslash bool
	flag.BoolVar(&escapeBackslash, "escape", true, "escape backslash")
	flag.Parse()

	cur, err := os.Getwd()
	if err != nil {
		fmt.Println(err)
		return
	}

	res := strings.Split(cur, "/")
	if len(res) == 1 {
		res = strings.Split(cur, "\\")
	}

	start := false
	pathList := []string{dockerGOPATH}
	for _, name := range res {
		if name == startFlagInPath {
			start = true
			continue
		}
		if start {
			pathList = append(pathList, name)
		}
	}

	targetPath := path.Join(pathList...)
	args := strings.Join(os.Args[1:], " ")

	if escapeBackslash {
		args = strings.Replace(args, "\\", "/", -1)
	}

	cmdStr := fmt.Sprintf(`docker run --rm --name golang -e GO111MODULE=auto -v %s:%s %s /bin/bash -c "cd %s && go %s"`,
		myGOPATH, dockerGOPATH, dockerGoTag, targetPath, args)

	fmt.Printf("\n%s\n\n", cmdStr)

	cmd := exec.Command("bash", "-c", cmdStr)
	var out bytes.Buffer
	cmd.Stdout = &out
	err = cmd.Run()
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(out.String())
}
