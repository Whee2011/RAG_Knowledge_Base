@echo off
title RAG Knowledge Base - Dependency Check

REM ============================================
REM RAG Knowledge Base Installer - Dependency Check
REM Version: v3.1
REM Date: 2026-04-16
REM Simplified: Only check core dependencies
REM ============================================

echo ============================================================
echo      RAG Knowledge Base Installer - Dependency Check v3.1
echo ============================================================
echo.

cd /d "%~dp0"

echo [1] Checking dependency configuration...
echo.

set "REQ_FILE=packages\requirements.txt"
if not exist "%REQ_FILE%" set "REQ_FILE=requirements.txt"

REM Core dependencies
set "PASS=0"
set "FAIL=0"

findstr /C:"chromadb" "%REQ_FILE%" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] ChromaDB not configured
    set /a FAIL+=1
) else (
    echo   [PASS] ChromaDB configured
    set /a PASS+=1
)

findstr /C:"Flask" "%REQ_FILE%" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Flask not configured
    set /a FAIL+=1
) else (
    echo   [PASS] Flask configured
    set /a PASS+=1
)

findstr /C:"pymupdf" "%REQ_FILE%" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] PyMuPDF not configured
    set /a FAIL+=1
) else (
    echo   [PASS] PyMuPDF configured
    set /a PASS+=1
)

findstr /C:"rapidocr" "%REQ_FILE%" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] RapidOCR not configured
    set /a FAIL+=1
) else (
    echo   [PASS] RapidOCR configured
    set /a PASS+=1
)

findstr /C:"onnxruntime" "%REQ_FILE%" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] ONNX Runtime not configured
    set /a FAIL+=1
) else (
    echo   [PASS] ONNX Runtime configured
    set /a PASS+=1
)

findstr /C:"numpy" "%REQ_FILE%" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] NumPy not configured
    set /a FAIL+=1
) else (
    echo   [PASS] NumPy configured
    set /a PASS+=1
)

findstr /C:"opencv" "%REQ_FILE%" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] OpenCV not configured
    set /a FAIL+=1
) else (
    echo   [PASS] OpenCV configured
    set /a PASS+=1
)

echo.
echo ============================================================
echo                  Results Summary
echo ============================================================
echo.
echo Passed: %PASS%
echo Failed: %FAIL%
echo.

if %FAIL% equ 0 (
    echo [SUCCESS] All core dependencies configured correctly!
    echo.
    echo RapidOCR replaces PaddleOCR - no protobuf conflict.
    echo Safe to distribute.
    exit /b 0
) else (
    echo [ERROR] Some dependencies missing or misconfigured!
    echo.
    echo Please check requirements.txt
    exit /b 1
)