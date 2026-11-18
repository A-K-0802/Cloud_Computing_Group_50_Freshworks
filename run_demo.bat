@echo off
title Group 50 - Serverless Live Web Demo
cd /d "%~dp0"
echo ========================================================
echo   Launching Group 50 Serverless Web Demo...
echo   URL: http://localhost:8000
echo ========================================================
python web_demo.py
pause
