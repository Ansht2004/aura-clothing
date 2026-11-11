@echo off
echo ===================================================
echo Running Aura Apparel Test Suite (Pytest)...
echo ===================================================
cd /d "%~dp0backend"
venv\Scripts\python.exe -m pytest --rootdir="%~dp0backend" -v
pause
