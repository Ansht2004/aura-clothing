@echo off
title Aura Apparel - 1-Click Launch Master
color 0E
echo ================================================================
echo       AURA APPAREL LUXURY STORE - ONE-CLICK LAUNCH MASTER
echo ================================================================
echo.
echo [1/4] Ensuring clean ports (clearing any stale processes on 5000 & 3000)...
powershell -NoProfile -Command "5000, 3000 | ForEach-Object { $p = $_; Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue } }"
timeout /t 1 /nobreak >nul

echo [2/4] Starting Flask REST Backend on port 5000...
start "Aura Backend API (Port 5000)" "%~dp0run_backend.bat"

echo [*] Waiting for Backend to be online and healthy...
powershell -NoProfile -Command "$ready = $false; for ($i=0; $i -lt 15; $i++) { try { $res = Invoke-WebRequest -Uri 'http://127.0.0.1:5000/api/products?per_page=1' -UseBasicParsing -TimeoutSec 2; if ($res.StatusCode -eq 200) { $ready = $true; break; } } catch {}; Start-Sleep -Milliseconds 800 }; if (-not $ready) { Write-Host '[WARN] Backend startup took longer than expected.' } else { Write-Host '[OK] Backend is healthy and serving requests!' }"

echo.
echo [3/4] Starting Vite Frontend on port 3000...
start "Aura Frontend Client (Port 3000)" "%~dp0run_frontend.bat"

echo [*] Waiting for Frontend webserver...
powershell -NoProfile -Command "$ready = $false; for ($i=0; $i -lt 15; $i++) { try { $res = Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing -TimeoutSec 2; if ($res.StatusCode -eq 200) { $ready = $true; break; } } catch {}; Start-Sleep -Milliseconds 800 }; if ($ready) { Write-Host '[OK] Frontend is online and ready!' }"

echo.
echo [4/4] Opening Aura Apparel in your browser...
start http://localhost:3000

echo.
echo ================================================================
echo  All systems running! 
echo  - Frontend: http://localhost:3000
echo  - Backend:  http://127.0.0.1:5000
echo.
echo  To stop everything cleanly, run STOP_AURA_CLOTHING.bat
echo ================================================================
pause
