@echo off
echo ===================================================
echo Seeding Aura Apparel Database (>1,500 Records)...
echo ===================================================
cd /d "%~dp0backend"
venv\Scripts\python.exe seed_data.py
pause
