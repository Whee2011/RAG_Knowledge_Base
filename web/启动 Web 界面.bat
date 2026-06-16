@echo off
chcp 65001 >nul
title RAG Knowledge Base Web Interface

echo ============================================================
echo    RAG Knowledge Base Web Interface Launcher
echo ============================================================
echo.

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "WEB_DIR=%SCRIPT_DIR%"
set "APP_DIR=%WEB_DIR%\.."
set "PYTHON_EXE=%APP_DIR%\python_embedded\python.exe"
set "WHEELS_DIR=%APP_DIR%\packages\requirements_cp311"

REM Check Python exists
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python not found at %PYTHON_EXE%
    echo.
    echo Please reinstall the application.
    pause
    exit /b 1
)

echo Checking Python environment...
"%PYTHON_EXE%" --version
echo.

echo Checking dependencies...
"%PYTHON_EXE%" -c "import flask, chromadb, pymupdf, rapidocr_onnxruntime; print('All dependencies OK')" 2>nul
if errorlevel 1 (
    echo Some dependencies are missing.
    echo.
    echo Installing from local packages...
    "%PYTHON_EXE%" -m pip install --no-index --find-links="%WHEELS_DIR%" -r "%APP_DIR%\packages\requirements.txt"
    if errorlevel 1 (
        echo.
        echo Installation failed. Please run install.bat manually.
        pause
        exit /b 1
    )
)
echo.

echo ============================================================
echo Starting Web Server...
echo ============================================================
echo.
echo Access URL: http://localhost:5000
echo LAN Access: http://YOUR_IP:5000
echo.
echo Press Ctrl+C to stop
echo.
echo ============================================================
echo.

cd /d "%WEB_DIR%"
"%PYTHON_EXE%" web_app.py

pause