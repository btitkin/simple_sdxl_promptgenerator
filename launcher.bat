## launcher.bat
```bat
@echo off
REM Launcher for Ultra Detailed NSFW SDXL Prompt Suite

echo ===========================================
echo Launching Ultra Detailed NSFW SDXL Prompt Suite
echo ===========================================
echo.

REM Ensure Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.8+ and add it to PATH.
    pause
    exit /b 1
)

REM Move to script directory
cd /d "%~dp0"

REM Installing dependencies
pip show customtkinter >nul 2>&1 || pip install customtkinter
pip show pyperclip >nul 2>&1 || pip install pyperclip
pip show pillow >nul 2>&1 || pip install pillow
pip show requests >nul 2>&1 || pip install requests

REM Running the main application
python main.py

pause
```