@echo off
title Aura Apparel - Backend API Server (Port 5000)
color 0A
echo ================================================================
echo           AURA APPAREL - BACKEND FLASK REST API
echo ================================================================
echo [*] Checking and freeing Port 5000...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }"

echo [*] Starting Flask API on http://127.0.0.1:5000 ...
cd /d "%~dp0backend"
venv\Scripts\python.exe app.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Flask server exited with code %ERRORLEVEL%.
    pause
)
