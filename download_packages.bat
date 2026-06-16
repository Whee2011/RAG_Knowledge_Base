@echo off
chcp 65001 >nul
title RAG 知识库 - 下载离线依赖包

REM ============================================
REM 离线依赖包下载脚本
REM 最后更新：2026-04-03
REM ============================================

setlocal DisableDelayedExpansion

echo ╔════════════════════════════════════════════════════╗
echo ║       下载 RAG 知识库离线依赖包                    ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM ==================== 获取脚本所在目录 ====================
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

cd /d "%SCRIPT_DIR%"

REM ==================== 创建目录 ====================
echo 创建下载目录...
if not exist "packages" mkdir "packages"
if not exist "packages\requirements" mkdir "packages\requirements"

echo ✅ 目录创建完成
echo.

REM ==================== 下载 VC++ 运行库 ====================
echo [1/3] 下载 Visual C++ 运行库...
set "VCREDIST_URL=https://aka.ms/vs/17/release/vc_redist.x64.exe"

if exist "packages\vcredist_x64.exe" (
    echo   ✅ 文件已存在，跳过
) else (
    echo   正在下载...
    powershell -Command "& {Invoke-WebRequest -Uri '%VCREDIST_URL%' -OutFile 'packages\vcredist_x64.exe'}" 2>nul
    if errorlevel 1 (
        echo   ❌ 下载失败
        echo   请手动下载：%VCREDIST_URL%
    ) else (
        echo   ✅ 下载完成
        for %%I in ("packages\vcredist_x64.exe") do echo   大小：%%~zI 字节
    )
)
echo.

REM ==================== 下载 Python 嵌入式 ====================
echo [2/3] 下载 Python 3.10 嵌入式...
set "PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip"

if exist "packages\python_embedded.zip" (
    echo   ✅ 文件已存在，跳过
) else (
    echo   正在下载...
    powershell -Command "& {Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile 'packages\python_embedded.zip'}" 2>nul
    if errorlevel 1 (
        echo   ❌ 下载失败
        echo   请手动下载：%PYTHON_URL%
    ) else (
        echo   ✅ 下载完成
        for %%I in ("packages\python_embedded.zip") do echo   大小：%%~zI 字节
    )
)
echo.

REM ==================== 下载 pip 依赖包 ====================
echo [3/3] 下载 Python 依赖包...
echo.

REM 创建 requirements.txt
echo 创建 requirements.txt...
(
    echo # RAG 知识库核心依赖
    echo chromadb>=0.4.0
    echo flask>=2.3.0
    echo pymupdf>=1.23.0
    echo numpy^<2.0
    echo pandas>=2.0.0
    echo python-docx>=0.8.11
    echo openpyxl>=3.1.0
    echo pillow>=10.0.0
    echo requests>=2.31.0
    echo pyyaml>=6.0
    echo.
    echo # OCR 依赖（可选）
    echo rapidocr
    echo onnxruntime
) > "packages\requirements.txt"

echo ✅ requirements.txt 创建完成
echo.

REM 检查是否有 Python 可用
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，无法下载依赖包
    echo 请先安装 Python 或使用系统 Python
    echo.
    echo 依赖包将在安装时在线下载
    goto :summary
)

echo 使用系统 Python 下载依赖包...
echo.

REM 升级 pip
echo 升级 pip...
python -m pip install --upgrade pip --quiet

REM 下载依赖包到本地目录
echo 下载依赖包到 packages\requirements...
echo 这可能需要几分钟...
echo.

python -m pip download -r "packages\requirements.txt" -d "packages\requirements" --no-cache-dir
if errorlevel 1 (
    echo.
    echo ⚠️  部分依赖包下载失败
    echo 请检查网络连接
    echo.
    echo 安装时会尝试在线下载剩余依赖包
) else (
    echo ✅ 所有依赖包下载完成
)

echo.

:summary
    echo ════════════════════════════════════════════════════
    echo 下载总结
    echo ════════════════════════════════════════════════════
    echo.
    
    echo 已下载文件:
    echo.
    
    if exist "packages\vcredist_x64.exe" (
        for %%I in ("packages\vcredist_x64.exe") do echo   ✅ vcredist_x64.exe (%%~zI 字节)
    ) else (
        echo   ❌ vcredist_x64.exe (未下载)
    )
    
    if exist "packages\python_embedded.zip" (
        for %%I in ("packages\python_embedded.zip") do echo   ✅ python_embedded.zip (%%~zI 字节)
    ) else (
        echo   ❌ python_embedded.zip (未下载)
    )
    
    if exist "packages\requirements.txt" (
        echo   ✅ requirements.txt
    )
    
    if exist "packages\requirements" (
        for /f "tokens=*" %%i in ('dir /b "packages\requirements\*.whl" 2^>nul ^| find /c /v ""') do echo   ✅ 依赖包 (%%i 个.whl 文件)
    )
    
    echo.
    echo 包位置：%SCRIPT_DIR%\packages\
    echo.
    echo ════════════════════════════════════════════════════
    echo.
    echo 下一步:
    echo   运行 install.bat 开始安装
    echo.

pause
exit /b 0
