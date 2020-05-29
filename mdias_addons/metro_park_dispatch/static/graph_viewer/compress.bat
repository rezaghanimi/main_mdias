@echo off

cd /d %~dp0
DEL skin
7z.exe a -r archive.zip -pcdtct123456  .\*
RENAME archive.zip skin