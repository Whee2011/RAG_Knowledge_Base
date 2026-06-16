@echo off
chcp 65001 >nul
title RAG 知识库 - 服务状态检测

REM ============================================
REM RAG 知识库系统 - 状态检测脚本
REM 最后更新：2026-04-03
REM ============================================

setlocal DisableDelayedExpansion

echo ╔════════════════════════════════════════════════════╗
echo ║       RAG 知识库系统 - 服务状态                    ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM ==================== 获取脚本所在目录 ====================
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

cd /d "%SCRIPT_DIR%"

REM ==================== 读取配置 ====================
if exist "%SCRIPT_DIR%\config.yaml" (
    for /f "tokens=2 delims=: " %%i in ('findstr "^web_port:" "%SCRIPT_DIR%\config.yaml"') do set "WEB_PORT=%%i"
    for /f "tokens=2 delims=: " %%i in ('findstr "^documents_path:" "%SCRIPT_DIR%\config.yaml"') do set "DOC_PATH=%%i"
) else (
    set "WEB_PORT=5000"
    set "DOC_PATH=未知"
)

echo 配置信息:
echo   安装路径：%SCRIPT_DIR%
echo   文档路径：%DOC_PATH%
echo   Web 端口：%WEB_PORT%
echo.

REM ==================== 服务状态检测 ====================
echo ════════════════════════════════════════════════════
echo 服务状态:
echo ════════════════════════════════════════════════════
echo.

REM LM Studio 状态
echo [1/4] LM Studio 服务
netstat -ano | findstr ":1234" >nul 2>&1
if errorlevel 1 (
    echo   状态：❌ 未运行
    echo   端口：1234 未监听
) else (
    for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":1234"') do set "LM_PID=%%i"
    echo   状态：✅ 运行中
    echo   端口：1234
    echo   PID: %LM_PID%
)
echo.

REM RAG Web 服务状态
echo [2/4] RAG Web 服务
netstat -ano | findstr ":%WEB_PORT%" >nul 2>&1
if errorlevel 1 (
    echo   状态：❌ 未运行
    echo   端口：%WEB_PORT% 未监听
) else (
    for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":%WEB_PORT%"') do set "WEB_PID=%%i"
    echo   状态：✅ 运行中
    echo   端口：%WEB_PORT%
    echo   PID: %WEB_PID%
)
echo.

REM OCR 自动处理服务状态
echo [3/4] OCR 自动处理服务
tasklist /FI "WINDOWTITLE eq RAG OCR*" 2>nul | findstr "python" >nul 2>&1
if errorlevel 1 (
    echo   状态：ℹ️  未运行（可选服务）
) else (
    for /f "tokens=2" %%i in ('tasklist /FI "WINDOWTITLE eq RAG OCR*" /FO CSV ^| findstr "python"') do set "OCR_PID=%%i"
    echo   状态：✅ 运行中
    echo   PID: %OCR_PID%
)
echo.

REM Python 环境状态
echo [4/4] Python 环境
if exist "%SCRIPT_DIR%\python_embedded\python.exe" (
    echo   类型：嵌入式 Python
    echo   路径：%SCRIPT_DIR%\python_embedded\python.exe
    "%SCRIPT_DIR%\python_embedded\python.exe" --version
) else if exist "python" (
    echo   类型：系统 Python
    python --version
) else (
    echo   状态：❌ 未找到 Python
)
echo.

REM ==================== 文件系统检测 ====================
echo ════════════════════════════════════════════════════
echo 文件系统:
echo ════════════════════════════════════════════════════
echo.

if exist "%DOC_PATH%" (
    echo 文档目录：%DOC_PATH%
    echo   状态：✅ 存在
    
    REM 统计文件数量
    for /f "tokens=*" %%i in ('dir /b "%DOC_PATH%" 2^>nul ^| find /c /v ""') do set "FILE_COUNT=%%i"
    echo   文件数：%FILE_COUNT%
    
    REM 检查 ChromaDB
    if exist "%DOC_PATH%\.rag\chroma_db" (
        echo.
        echo ChromaDB: ✅ 已初始化
    ) else (
        echo.
        echo ChromaDB: ⚠️  未初始化（首次运行会自动创建）
    )
) else (
    echo 文档目录：%DOC_PATH%
    echo   状态：❌ 不存在
)
echo.

REM ==================== 依赖包检测 ====================
echo ════════════════════════════════════════════════════
echo 依赖包:
echo ════════════════════════════════════════════════════
echo.

if exist "%SCRIPT_DIR%\python_embedded\python.exe" (
    set "PYTHON_EXE=%SCRIPT_DIR%\python_embedded\python.exe"
) else (
    set "PYTHON_EXE=python"
)

%PYTHON_EXE% -c "import chromadb" 2>nul && echo   chromadb     : ✅ 已安装 || echo   chromadb     : ❌ 未安装
%PYTHON_EXE% -c "import flask" 2>nul && echo   flask        : ✅ 已安装 || echo   flask        : ❌ 未安装
%PYTHON_EXE% -c "import pymupdf" 2>nul && echo   pymupdf      : ✅ 已安装 || echo   pymupdf      : ❌ 未安装
%PYTHON_EXE% -c "from rapidocr import RapidOCR" 2>nul && echo   rapidocr     : ✅ 已安装 || echo   rapidocr     : ⚠️  未安装（OCR 需要）
%PYTHON_EXE% -c "from rapidocr import RapidOCR; ocr=RapidOCR()" 2>nul && echo   OCR 引擎     : ✅ 正常 || echo   OCR 引擎     : ⚠️  未初始化
echo.

REM ==================== 快速操作 ====================
echo ════════════════════════════════════════════════════
echo 快速操作:
echo ════════════════════════════════════════════════════
echo.
echo   1. 启动所有服务 (start_all.bat)
echo   2. 停止所有服务 (stop_all.bat)
echo   3. 刷新此状态 (R)
echo   4. 退出 (Q)
echo.

set /p action="请选择操作："

if /i "%action%"=="1" (
    start "%SCRIPT_DIR%\start_all.bat" "%SCRIPT_DIR%\start_all.bat"
    exit /b 0
)

if /i "%action%"=="2" (
    start "%SCRIPT_DIR%\stop_all.bat" "%SCRIPT_DIR%\stop_all.bat"
    exit /b 0
)

if /i "%action%"=="R" (
    cls
    goto :EOF
)

if /i "%action%"=="Q" (
    exit /b 0
)

echo.
pause
exit /b 0
