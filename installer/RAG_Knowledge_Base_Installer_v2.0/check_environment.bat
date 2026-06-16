@echo off
chcp 65001 >nul
title RAG 知识库 - 环境检测

REM ============================================
REM RAG 知识库系统 - 环境检测脚本
REM 最后更新：2026-04-03
REM ============================================

setlocal DisableDelayedExpansion

echo ╔════════════════════════════════════════════════════╗
echo ║       RAG 知识库系统 - 环境检测                    ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM ==================== 获取脚本所在目录 ====================
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

cd /d "%SCRIPT_DIR%"

REM ==================== 创建报告文件 ====================
set "REPORT_FILE=%SCRIPT_DIR%\environment_report.txt"
echo RAG 知识库系统 - 环境检测报告 > "%REPORT_FILE%"
echo 生成时间：%date% %time% >> "%REPORT_FILE%"
echo ============================================ >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

REM ==================== 系统信息 ====================
echo [1/10] 检测系统信息...
echo.
echo === 系统信息 === >> "%REPORT_FILE%"

echo 操作系统:
ver >> "%REPORT_FILE%"
echo   Windows 版本：%ver%

echo 计算机名:
hostname >> "%REPORT_FILE%"

echo 用户:
echo %USERNAME% >> "%REPORT_FILE%"
echo   当前用户：%USERNAME%

echo 系统目录:
echo %WINDIR% >> "%REPORT_FILE%"

echo. >> "%REPORT_FILE%"

REM ==================== CPU 和内存 ====================
echo [2/10] 检测硬件信息...
echo.
echo === 硬件信息 === >> "%REPORT_FILE%"

REM CPU 信息
wmic cpu get name >> "%REPORT_FILE%" 2>nul
for /f "skip=1 tokens=*" %%i in ('wmic cpu get name 2^>nul') do (
    echo   CPU: %%i
    goto :cpu_done
)
:cpu_done

REM 内存信息
wmic memorychip get capacity >> "%TEMP%\mem.tmp" 2>nul
set /a TOTAL_MEM=0
for /f "tokens=*" %%i in ('type "%TEMP%\mem.tmp" 2^>nul ^| findstr "[0-9]"') do (
    set /a TOTAL_MEM+=%%i
)
set /a TOTAL_MEM_GB=TOTAL_MEM/1024/1024/1024
echo   内存：%TOTAL_MEM_GB% GB >> "%REPORT_FILE%"
echo   内存：约 %TOTAL_MEM_GB% GB

del "%TEMP%\mem.tmp" 2>nul

echo. >> "%REPORT_FILE%"

REM ==================== 磁盘空间 ====================
echo [3/10] 检测磁盘空间...
echo.
echo === 磁盘空间 === >> "%REPORT_FILE%"

for %%d in (C D E F) do (
    if exist "%%d:\" (
        for /f "tokens=3" %%s in ('dir /-c %%d:\ 2^>nul ^| find "字节"') do (
            echo   %%d: 盘 - 可用：%%s 字节 >> "%REPORT_FILE%"
        )
    )
)

echo.

REM ==================== Python 环境 ====================
echo [4/10] 检测 Python 环境...
echo.
echo === Python 环境 === >> "%REPORT_FILE%"

where python >nul 2>&1
if errorlevel 1 (
    echo   系统 Python: 未安装 >> "%REPORT_FILE%"
    echo   系统 Python: 未安装
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do (
        echo   系统 Python: %%i >> "%REPORT_FILE%"
        echo   系统 Python: %%i
    )
    for /f "tokens=*" %%i in ('where python') do (
        echo   Python 路径：%%i >> "%REPORT_FILE%"
    )
)

if exist "%SCRIPT_DIR%\python_embedded\python.exe" (
    echo   嵌入式 Python: 已安装 >> "%REPORT_FILE%"
    "%SCRIPT_DIR%\python_embedded\python.exe" --version
) else (
    echo   嵌入式 Python: 未安装 >> "%REPORT_FILE%"
    echo   嵌入式 Python: 未安装
)

echo. >> "%REPORT_FILE%"

REM ==================== Visual C++ 运行库 ====================
echo [5/10] 检测 Visual C++ 运行库...
echo.
echo === Visual C++ 运行库 === >> "%REPORT_FILE%"

set "VCREDIST_STATUS=未知"

if exist "C:\Windows\System32\vcruntime140.dll" (
    echo   vcruntime140.dll: 存在 >> "%REPORT_FILE%"
    echo   ✅ vcruntime140.dll: 存在
    set "VCREDIST_STATUS=已安装"
) else (
    echo   vcruntime140.dll: 缺失 >> "%REPORT_FILE%"
    echo   ❌ vcruntime140.dll: 缺失
    set "VCREDIST_STATUS=缺失"
)

if exist "C:\Windows\System32\msvcp140.dll" (
    echo   msvcp140.dll: 存在 >> "%REPORT_FILE%"
    echo   ✅ msvcp140.dll: 存在
) else (
    echo   msvcp140.dll: 缺失 >> "%REPORT_FILE%"
    echo   ❌ msvcp140.dll: 缺失
    set "VCREDIST_STATUS=缺失"
)

echo.
if "%VCREDIST_STATUS%"=="已安装" (
    echo   ✅ Visual C++ 运行库已安装
) else (
    echo   ❌ Visual C++ 运行库缺失
    echo   ⚠️  以下功能可能无法使用：
    echo      • RapidOCR (图片文字识别)
    echo      • PyMuPDF (PDF 文件处理)
    echo      • NumPy/Pandas (数据处理)
)

echo. >> "%REPORT_FILE%"

REM ==================== LM Studio ====================
echo [6/10] 检测 LM Studio...
echo.
echo === LM Studio === >> "%REPORT_FILE%"

if exist "%LOCALAPPDATA%\Programs\lm-studio\lm-studio.exe" (
    echo   安装状态：已安装 >> "%REPORT_FILE%"
    echo   安装路径：%LOCALAPPDATA%\Programs\lm-studio\ >> "%REPORT_FILE%"
    echo   ✅ LM Studio: 已安装
    set "LM_STUDIO_INSTALLED=1"
) else (
    echo   安装状态：未安装 >> "%REPORT_FILE%"
    echo   ❌ LM Studio: 未安装
    set "LM_STUDIO_INSTALLED=0"
)

netstat -ano | findstr ":1234" >nul 2>&1
if errorlevel 1 (
    echo   服务状态：未运行 >> "%REPORT_FILE%"
    echo   ❌ LM Studio 服务：未运行
) else (
    for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":1234"') do (
        echo   服务状态：运行中 (PID: %%i) >> "%REPORT_FILE%"
        echo   ✅ LM Studio 服务：运行中 (PID: %%i)
    )
)

echo. >> "%REPORT_FILE%"

REM ==================== 已安装的依赖包 ====================
echo [7/10] 检测 Python 依赖包...
echo.
echo === Python 依赖包 === >> "%REPORT_FILE%"

if exist "%SCRIPT_DIR%\python_embedded\python.exe" (
    set "PYTHON_EXE=%SCRIPT_DIR%\python_embedded\python.exe"
) else (
    set "PYTHON_EXE=python"
)

%PYTHON_EXE% -c "import chromadb; print('chromadb:', chromadb.__version__)" 2>nul >> "%REPORT_FILE%" && echo   ✅ chromadb: 已安装 || echo   ❌ chromadb: 未安装
%PYTHON_EXE% -c "import flask; print('flask:', flask.__version__)" 2>nul >> "%REPORT_FILE%" && echo   ✅ flask: 已安装 || echo   ❌ flask: 未安装
%PYTHON_EXE% -c "import pymupdf; print('pymupdf:', pymupdf.__version__)" 2>nul >> "%REPORT_FILE%" && echo   ✅ pymupdf: 已安装 || echo   ❌ pymupdf: 未安装
%PYTHON_EXE% -c "import numpy; print('numpy:', numpy.__version__)" 2>nul >> "%REPORT_FILE%" && echo   ✅ numpy: 已安装 || echo   ❌ numpy: 未安装
%PYTHON_EXE% -c "import pandas; print('pandas:', pandas.__version__)" 2>nul >> "%REPORT_FILE%" && echo   ✅ pandas: 已安装 || echo   ❌ pandas: 未安装
%PYTHON_EXE% -c "from rapidocr import RapidOCR; print('rapidocr: OK')" 2>nul >> "%REPORT_FILE%" && echo   ✅ rapidocr: 已安装 || echo   ⚠️  rapidocr: 未安装
%PYTHON_EXE% -c "from rapidocr import RapidOCR; ocr=RapidOCR(); print('OCR: OK')" 2>nul >> "%REPORT_FILE%" && echo   ✅ OCR 引擎: 正常 || echo   ⚠️  OCR 引擎: 未安装

echo. >> "%REPORT_FILE%"

REM ==================== 网络连通性 ====================
echo [8/10] 检测网络连通性...
echo.
echo === 网络连通性 === >> "%REPORT_FILE%"

ping -n 1 -w 1000 www.baidu.com >nul 2>&1
if errorlevel 1 (
    echo   互联网：❌ 无法访问 >> "%REPORT_FILE%"
    echo   ❌ 互联网：无法访问
) else (
    echo   互联网：✅ 正常 >> "%REPORT_FILE%"
    echo   ✅ 互联网：正常
)

curl -s -o nul -w "%%{http_code}" http://127.0.0.1:1234/v1/models 2>nul | findstr "200" >nul 2>&1
if errorlevel 1 (
    echo   LM Studio API: ❌ 无法访问 >> "%REPORT_FILE%"
    echo   ❌ LM Studio API: 无法访问
) else (
    echo   LM Studio API: ✅ 正常 >> "%REPORT_FILE%"
    echo   ✅ LM Studio API: 正常
)

echo. >> "%REPORT_FILE%"

REM ==================== 端口占用 ====================
echo [9/10] 检测端口占用...
echo.
echo === 端口占用 === >> "%REPORT_FILE%"

echo 端口 1234 (LM Studio): >> "%REPORT_FILE%"
netstat -ano | findstr ":1234" >> "%REPORT_FILE%" 2>nul || echo   未占用 >> "%REPORT_FILE%"

echo 端口 5000 (RAG Web): >> "%REPORT_FILE%"
netstat -ano | findstr ":5000" >> "%REPORT_FILE%" 2>nul || echo   未占用 >> "%REPORT_FILE%"

echo.

REM ==================== 总结 ====================
echo [10/10] 生成检测报告...
echo.
echo === 检测总结 === >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

set "ISSUE_COUNT=0"

if "%LM_STUDIO_INSTALLED%"=="0" (
    echo ⚠️  注意：LM Studio 未安装 >> "%REPORT_FILE%"
    set /a ISSUE_COUNT+=1
)

if "%VCREDIST_STATUS%"=="缺失" (
    echo ⚠️  注意：Visual C++ 运行库缺失 >> "%REPORT_FILE%"
    set /a ISSUE_COUNT+=1
)

if %ISSUE_COUNT%==0 (
    echo ✅ 所有检测项通过 >> "%REPORT_FILE%"
) else (
    echo ⚠️  发现 %ISSUE_COUNT% 个需要注意的问题 >> "%REPORT_FILE%"
)

echo. >> "%REPORT_FILE%"
echo 报告已保存：%REPORT_FILE% >> "%REPORT_FILE%"

echo.
echo ════════════════════════════════════════════════════
echo 检测完成！
echo ════════════════════════════════════════════════════
echo.
echo 报告已保存：%REPORT_FILE%
echo.
echo 是否打开报告文件？(Y/N)
set /p open_report=""
if /i "%open_report%"=="Y" (
    notepad "%REPORT_FILE%"
)

echo.
pause
exit /b 0
