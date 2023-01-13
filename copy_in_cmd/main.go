package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"golang.org/x/text/encoding/simplifiedchinese"
	"golang.org/x/text/transform"
	"io/ioutil"
	"os"
	"strings"
	"unicode/utf8"
)

// 管道的内容，位于 os.Stdin 里，通过 os.Stdin 的 mode 值来判断程序是否通过管道调用，然后通过 bufio 包获取数据
func HasStdin() ([][]byte, bool) {
	fileInfo, _ := os.Stdin.Stat()
	if (fileInfo.Mode() & os.ModeNamedPipe) != os.ModeNamedPipe {
		return nil, false
	}
	s := bufio.NewScanner(os.Stdin)
	resList := make([][]byte, 0, 0)
	for s.Scan() {
		resList = append(resList, s.Bytes())
	}
	return resList, true
}

func CleanBytes(data [][]byte) string {
	var retList []string
	for _, line := range data {
		resBytes := line
		if IsGbk(line) {
			resBytes, _ = GbkToUtf8(resBytes)
		}
		retList = append(retList, cleanInvalidByte(resBytes))
	}
	result := strings.Join(retList, "\n")
	return result
}

func cleanInvalidByte(b []byte) string {
	originStr := string(b)
	srcRunes := []rune(originStr)
	dstRunes := make([]rune, 0, len(srcRunes))
	for _, c := range srcRunes {
		if c >= 0 && c <= 31 {
			continue
		}
		if c == 127 {
			continue
		}
		dstRunes = append(dstRunes, c)
	}
	result := string(dstRunes)
	return result
}

func IsUtf8(s []byte) bool {
	return utf8.Valid(s)
}

func IsGbk(data []byte) bool {
	if IsUtf8(data) {
		return false
	}
	length := len(data)
	var i int = 0
	for i < length {
		if data[i] <= 0xff {
			i++
			continue
		} else {
			if data[i] >= 0x81 &&
				data[i] <= 0xfe &&
				data[i+1] >= 0x40 &&
				data[i+1] <= 0xfe &&
				data[i+1] != 0xf7 {
				i += 2
				continue
			} else {
				return false
			}
		}
	}
	return true
}

func GbkToUtf8(s []byte) ([]byte, error) {
	reader := transform.NewReader(bytes.NewReader(s), simplifiedchinese.GBK.NewDecoder())
	d, e := ioutil.ReadAll(reader)
	if e != nil {
		return nil, e
	}
	return d, nil
}

func toWslPath(p string) string {
	p = strings.Replace(p, "\\", "/", -1)
	tempList := strings.SplitN(p, ":", 2)
	res := fmt.Sprintf("/mnt/%s%s", strings.ToLower(tempList[0]), tempList[1])
	return res
}

func main() {
	var err error
	var data string
	var wsl bool
	flag.BoolVar(&wsl, "wsl", false, "to wsl path")
	flag.Parse()

	dataBytes, ok := HasStdin()
	data = CleanBytes(dataBytes)
	if !ok {
		data, err = os.Getwd()
		if err != nil {
			fmt.Println(err)
			return
		}
		if wsl {
			data = toWslPath(data)
		}
	}

	if err = WriteAll(data); err != nil {
		fmt.Println(err)
		return
	}
	// 在数据写入剪切板后还是将其返回,方便后续串联管道
	fmt.Println(data)
}
