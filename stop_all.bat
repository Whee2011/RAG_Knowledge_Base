@echo off
chcp 65001 >nul
title RAG 知识库 - 停止所有服务

REM ============================================
REM RAG 知识库系统 - 停止脚本
REM 最后更新：2026-04-03
REM ============================================

setlocal DisableDelayedExpansion

echo ╔════════════════════════════════════════════════════╗
echo ║       RAG 知识库系统 - 停止服务                    ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM ==================== 获取脚本所在目录 ====================
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

cd /d "%SCRIPT_DIR%"

REM ==================== 读取配置 ====================
if exist "%SCRIPT_DIR%\config.yaml" (
    for /f "tokens=2 delims=: " %%i in ('findstr "^web_port:" "%SCRIPT_DIR%\config.yaml"') do set "WEB_PORT=%%i"
) else (
    set "WEB_PORT=5000"
)

echo 配置信息:
echo   Web 端口：%WEB_PORT%
echo.

REM ==================== 停止 RAG Web 服务 ====================
echo [1/3] 停止 RAG Web 服务...

for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":%WEB_PORT%"') do (
    set "WEB_PID=%%i"
    echo 发现 Web 服务进程：%WEB_PID%
    taskkill /F /PID %%i 2>nul
    if errorlevel 1 (
        echo ⚠️  无法终止进程 %%i
    ) else (
        echo ✅ 已终止进程 %%i
    )
)

REM 检查是否还有残留进程
timeout /t 2 /nobreak >nul
netstat -ano | findstr ":%WEB_PORT%" >nul 2>&1
if errorlevel 1 (
    echo ✅ RAG Web 服务已停止
) else (
    echo ⚠️  RAG Web 服务可能仍在运行
)
echo.

REM ==================== 停止 OCR 自动处理服务 ====================
echo [2/3] 停止 OCR 自动处理服务...

for /f "tokens=2" %%i in ('tasklist /FI "WINDOWTITLE eq RAG OCR*" /FO CSV ^| findstr "python"') do (
    set "OCR_PID=%%i"
    echo 发现 OCR 服务进程：%%i
    taskkill /F /PID %%i 2>nul
    if errorlevel 1 (
        echo ⚠️  无法终止进程 %%i
    ) else (
        echo ✅ 已终止进程 %%i
    )
)

echo ✅ OCR 服务已停止
echo.

REM ==================== 验证所有服务已停止 ====================
echo [3/3] 验证服务状态...
echo.
echo ════════════════════════════════════════════════════
echo 服务状态:
echo ════════════════════════════════════════════════════

netstat -ano | findstr ":%WEB_PORT%" >nul 2>&1 && echo   ⚠️  RAG Web 服务    : 仍在运行 || echo   ✅ RAG Web 服务    : 已停止

tasklist /FI "WINDOWTITLE eq RAG OCR*" 2>nul | findstr "python" >nul 2>&1 && echo   ⚠️  OCR 服务        : 仍在运行 || echo   ✅ OCR 服务        : 已停止

echo ════════════════════════════════════════════════════
echo.
echo 所有 RAG 服务已停止
echo.
echo ⚠️  注意：LM Studio 未停止（需手动关闭）
echo.

pause
exit /b 0
