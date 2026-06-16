@echo off
chcp 65001 >nul
title RAG Knowledge Base - Dependency Installer

echo ============================================================
echo    RAG Knowledge Base - Dependency Installer v3.1
echo ============================================================
echo.

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PYTHON_EXE=%SCRIPT_DIR%\python_embedded\python.exe"
set "PACKAGES_DIR=%SCRIPT_DIR%\packages"
set "WHEELS_DIR=%PACKAGES_DIR%\requirements_cp311"

echo Install directory: %SCRIPT_DIR%
echo Python location: %PYTHON_EXE%
echo.

REM Check Python exists
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python embedded not found!
    echo Expected location: %PYTHON_EXE%
    echo.
    echo Please reinstall using RAG_Knowledge_Base_v3.1_Setup.exe
    pause
    exit /b 1
)

echo Python version:
"%PYTHON_EXE%" --version
echo.

REM Check pip
"%PYTHON_EXE%" -m pip --version 2>nul
if errorlevel 1 (
    echo Installing pip...
    "%PYTHON_EXE%" "%PACKAGES_DIR%\get-pip.py" --no-warn-script-location
    if errorlevel 1 (
        echo ERROR: Failed to install pip
        pause
        exit /b 1
    )
)
echo.

echo ============================================================
echo Installing dependencies...
echo ============================================================
echo.
echo This may take several minutes...
echo.

REM Install all wheel packages
"%PYTHON_EXE%" -m pip install --no-warn-script-location --no-index --find-links="%WHEELS_DIR%" -r "%PACKAGES_DIR%\requirements.txt"

if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed
    echo.
    echo Please check:
    echo 1. Wheel files exist in %WHEELS_DIR%
    echo 2. requirements.txt is valid
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Installation completed!
echo ============================================================
echo.
echo Installed packages:
"%PYTHON_EXE%" -m pip list --format=columns
echo.
echo Next steps:
echo 1. Configure config/.env file
echo 2. Run start_all.bat to start services
echo 3. Access http://localhost:5000
echo.

pause