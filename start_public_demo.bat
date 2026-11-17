@echo off
title Group 50 - Public Serverless Web Demo (All Devices)
cd /d "%~dp0"

echo ========================================================
echo   1. Starting Local Server on Port 8000...
echo ========================================================
start "" /b python web_demo.py

timeout /t 2 >nul

echo ========================================================
echo   2. Generating Public HTTPS URL + QR Code...
echo   Open this URL or scan the QR Code on ANY phone/laptop!
echo   (Press Ctrl+C to stop)
echo ========================================================
echo.

ssh -o StrictHostKeyChecking=no -p 443 -R0:localhost:8000 qr@a.pinggy.io

pause
