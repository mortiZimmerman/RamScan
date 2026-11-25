@echo off
title RAM Scanner
cd /d "%~dp0"
where python >nul 2>nul || (echo Necesitas Python: https://www.python.org/downloads/ & pause & exit /b)
python -c "import psutil" 2>nul || python -m pip install -q psutil
python ram_scanner.py
pause
