@echo off
echo Check for Python 3.11...
py -3.11 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3.11 is not found via 'py -3.11'.
    echo Please install Python 3.11 or ensure the Python Launcher is installed.
    echo Falling back to 'python'...
    python VigilantiAI.py
) else (
    echo Launching SafeDrive with Python 3.11...
    py -3.11 VigilantiAI.py
)
pause
