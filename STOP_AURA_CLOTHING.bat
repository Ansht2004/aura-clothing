@echo off
title Aura Apparel - Stop All Services
color 0C
echo ================================================================
echo           AURA APPAREL - STOPPING ALL RUNNING SERVICES
echo ================================================================
echo [*] Terminating any processes on Port 5000 (Backend Flask)...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue; Write-Host \"[KILLED] Process PID $_ on port 5000\" }"

echo [*] Terminating any processes on Port 3000 (Frontend Vite)...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue; Write-Host \"[KILLED] Process PID $_ on port 3000\" }"

echo.
echo ================================================================
echo  Ports 5000 and 3000 are now completely free and clean!
echo ================================================================
timeout /t 3
