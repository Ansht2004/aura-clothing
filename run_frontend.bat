@echo off
title Aura Apparel - Frontend Vite Client (Port 3000)
color 0B
echo ================================================================
echo           AURA APPAREL - FRONTEND REACT APPLICATION
echo ================================================================
echo [*] Checking and freeing Port 3000...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }"

echo [*] Starting Vite Dev Server on http://localhost:3000 ...
cd /d "%~dp0frontend"
call npm run dev
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Frontend dev server exited with code %ERRORLEVEL%.
    pause
)
