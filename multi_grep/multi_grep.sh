#!/bin/bash

# usage: mutli_grep.sh ./ selenium cookie
if [ $# -le 1 ]; 
then
    echo "argument -le 1"
    exit 8
fi

cmd="grep -nirl \"$2\" \"$1\""

for i in "${@:3}";
do 
    append=" | xargs -d '\n' grep -Hnil \"${i}\""
    cmd=$cmd$append
done

echo ""
echo $cmd #just like: grep -nirl "selenium" "./" | xargs -d '\n' grep -Hnil "cookie"
echo ""

eval $cmd