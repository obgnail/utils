rem @echo off
set filename=D:\myshare\Dropbox\root\md\_Temp\textCollector\textCollector.md
echo ================================= >>%filename%
date /t >>%filename%
time /t >>%filename%
powershell get-clipboard >>%filename%