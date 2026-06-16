@echo off
chcp 65001 >nul
title RAG Knowledge Base - Start All Services

REM ============================================
REM RAG Knowledge Base - Start Script v3.1
REM Date: 2026-04-16
REM ============================================

setlocal DisableDelayedExpansion

echo ============================================================
echo    RAG Knowledge Base - Start All Services
echo ============================================================
echo.

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "PYTHON_EXE=%SCRIPT_DIR%\python_embedded\python.exe"

cd /d "%SCRIPT_DIR%"

echo Install directory: %SCRIPT_DIR%
echo Python location: %PYTHON_EXE%
echo.

REM Check Python exists
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python not found at %PYTHON_EXE%
    echo Please run install.bat first.
    pause
    exit /b 1
)

REM Check config file
if not exist "%SCRIPT_DIR%\config\.env" (
    echo WARNING: Config file not found: %SCRIPT_DIR%\config\.env
    echo Using default settings...
    set "WEB_PORT=5000"
    set "LMSTUDIO_URL=http://127.0.0.1:1234"
) else (
    REM Read config from .env
    for /f "usebackq tokens=*" %%i in (`powershell -Command "(Get-Content '%SCRIPT_DIR%\config\.env' | Where-Object {$_ -match '^WEB_PORT='} | ForEach-Object {$_ -replace 'WEB_PORT=', ''})"`) do set "WEB_PORT=%%i"
    for /f "usebackq tokens=*" %%i in (`powershell -Command "(Get-Content '%SCRIPT_DIR%\config\.env' | Where-Object {$_ -match '^LMSTUDIO_BASE_URL='} | ForEach-Object {$_ -replace 'LMSTUDIO_BASE_URL=', ''})"`) do set "LMSTUDIO_URL=%%i"
)

if not defined WEB_PORT set "WEB_PORT=5000"
if not defined LMSTUDIO_URL set "LMSTUDIO_URL=http://127.0.0.1:1234"

echo Config:
echo   Web Port: %WEB_PORT%
echo   LM Studio: %LMSTUDIO_URL%
echo.

REM Check LM Studio
echo [1/4] Checking LM Studio service...
for /f "tokens=2 delims=:" %%i in ("%LMSTUDIO_URL%") do set "LMSTUDIO_PORT=%%i"
set "LMSTUDIO_PORT=%LMSTUDIO_PORT:/=%"

netstat -ano | findstr ":%LMSTUDIO_PORT%" >nul 2>&1
if errorlevel 1 (
    echo WARNING: LM Studio not running (port %LMSTUDIO_PORT%)
    echo Please start LM Studio and load a model.
    echo.
) else (
    echo OK: LM Studio running
)
echo.

REM Start Web service
echo [2/4] Starting RAG Web service...

netstat -ano | findstr ":%WEB_PORT%" >nul 2>&1
if errorlevel 1 (
    echo Starting Web service...
    start "RAG Web Service" "%PYTHON_EXE%" "%SCRIPT_DIR%\web\web_app.py"
    
    timeout /t 5 /nobreak >nul
    
    netstat -ano | findstr ":%WEB_PORT%" >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Web service failed to start
        pause
        exit /b 1
    ) else (
        echo OK: Web service started (port %WEB_PORT%)
    )
) else (
    echo OK: Web service already running
)
echo.

REM Verify services
echo [3/4] Verifying service status...
echo.
echo ============================================================
echo Service Status:
echo ============================================================

netstat -ano | findstr ":%LMSTUDIO_PORT%" >nul 2>&1 && echo   [OK] LM Studio    : Running (port %LMSTUDIO_PORT%) || echo   [WARN] LM Studio   : Not running
netstat -ano | findstr ":%WEB_PORT%" >nul 2>&1 && echo   [OK] RAG Web      : Running (port %WEB_PORT%) || echo   [FAIL] RAG Web    : Not running

echo ============================================================
echo.
echo Install directory: %SCRIPT_DIR%
echo Access URL: http://localhost:%WEB_PORT%
echo.
echo Press Ctrl+C to stop services.
echo.

REM Open browser
echo [4/4] Opening Web interface...
timeout /t 2 /nobreak >nul
start http://localhost:%WEB_PORT%

echo Done. Press any key to close this window (services will keep running).
pause >nul

exit /b 0