@echo off
@set PATH=%PATH%;%~dp0bin\arm64

title Win64 OpenSSL for ARM Command Prompt
echo Win64 OpenSSL for ARM Command Prompt
echo.
openssl version -a
echo.

%SystemDrive%
cd %UserProfile%

cmd.exe /K
