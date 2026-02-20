@echo off
REM DARK8 OS - Setup Environment (Windows)

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo 🖤 DARK8 OS - Setup Environment
echo ================================
echo.

REM Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

python --version
echo ✓ Python found

REM Create virtual environment
echo [2/4] Creating virtual environment...
if not exist "%PROJECT_ROOT%\venv" (
    python -m venv "%PROJECT_ROOT%\venv"
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment exists
)

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
echo ✓ Virtual environment activated

REM Install dependencies
echo [4/4] Installing dependencies...
python -m pip install --upgrade pip setuptools wheel
pip install -r "%PROJECT_ROOT%\requirements.txt"
echo ✓ Dependencies installed

REM Create .env if not exists
if not exist "%PROJECT_ROOT%\.env" (
    echo.
    echo Creating .env from template...
    copy "%PROJECT_ROOT%\.env.example" "%PROJECT_ROOT%\.env"
    echo ✓ .env created (edit as needed)
)

echo.
echo 🖤 Setup complete!
echo.
echo Next steps:
echo   1. Activate environment: venv\Scripts\activate.bat
echo   2. Install Ollama: https://ollama.ai
echo   3. Run: python -m dark8_core
echo.
pause
