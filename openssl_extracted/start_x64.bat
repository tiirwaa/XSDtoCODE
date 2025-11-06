@echo off
@set PATH=%PATH%;%~dp0bin\x64

title Win64 OpenSSL Command Prompt
echo Win64 OpenSSL Command Prompt
echo.
openssl version -a
echo.

%SystemDrive%
cd %UserProfile%

cmd.exe /K
