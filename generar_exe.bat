@echo off
call .venv\Scripts\activate.bat
pyinstaller .\exe.spec --noconfirm
if not exist dist\XSDtoCODE\_internal (
    mkdir dist\XSDtoCODE\_internal
)
copy /Y xsd2php.phar dist\XSDtoCODE\_internal\xsd2php.phar
