@echo off
echo === Descargando dependencias ===
composer require goetas-webservices/xsd2php

echo === Instalando box ===
composer global require humbug/box

echo === Creando box.json ===
(
echo {
echo   "main": "vendor/goetas-webservices/xsd2php/src/Console/Application.php",
echo   "output": "xsd2php.phar",
echo   "compression": "GZ",
echo   "stub": true
echo }
) > box.json

echo === Compilando .phar ===
box compile

echo.
echo ✅ Listo! Se generó: xsd2php.phar
echo.
pause