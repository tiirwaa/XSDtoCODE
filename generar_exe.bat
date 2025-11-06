call .venv\Scripts\activate.bat
pyinstaller .\exe.spec --noconfirm
copy xsd2php.phar.backup dist\XSDtoCODE\xsd2php.phar