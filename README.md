## adb_element

简单封装 uiautomator, 便于 adb 使用



## copy_in_cmd

将命令输出写到剪贴板，支持管道符。默认复制当前文件路径。



## totalcmd_skip_register_page

跳过 total commander 的注册页面



## multi_grep

使用 `mutli_grep.sh ./ selenium cookie` 快速构建出 `grep -nirl "selenium" "./" | xargs -d '\n' grep -Hnil "cookie"` 语句，搜索包含多个关键字的文件



## graphql_parser

解析 graphQL，提高可读性



## progress_bar

进度条


## dockergo

使用如下命令快速构建出 `docker run --rm --name golang -e GO111MODULE=auto -v /d/golang:/go golang:1.18 /bin/bash -c "cd /go/src/github.com/obgnail/tmp/go_test/temp_test && go run ../main.go"`
```bash
D:\golang\src\github.com\obgnail\tmp\go_test\temp_test
$ dockergo run ..\main.go
```
