@echo off
chcp 65001 >nul
title Visual C++ 运行库 - 检测与修复

REM ============================================
REM Visual C++ 运行库 - 修复工具
REM 最后更新：2026-04-03
REM ============================================

setlocal DisableDelayedExpansion

echo ╔════════════════════════════════════════════════════╗
echo ║   Visual C++ 运行库 - 检测与修复                   ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM ==================== 检查管理员权限 ====================
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  需要管理员权限运行
    echo.
    echo 请右键点击 fix_vcredist.bat，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)
echo ✅ 管理员权限确认
echo.

REM ==================== 检测 VC++ 状态 ====================
echo 检测 Visual C++ 运行库...
echo.

set "MISSING_DLLS="
set "VCREDIST_URL=https://aka.ms/vs/17/release/vc_redist.x64.exe"

REM 检查关键 DLL 文件
if not exist "C:\Windows\System32\vcruntime140.dll" (
    set "MISSING_DLLS=%MISSING_DLLS% vcruntime140.dll"
    echo ❌ 缺失：vcruntime140.dll
)

if not exist "C:\Windows\System32\msvcp140.dll" (
    set "MISSING_DLLS=%MISSING_DLLS% msvcp140.dll"
    echo ❌ 缺失：msvcp140.dll
)

if not exist "C:\Windows\System32\vcruntime140_1.dll" (
    echo ⚠️  缺失：vcruntime140_1.dll (可选)
)

echo.

if "%MISSING_DLLS%"=="" (
    echo ✅ Visual C++ 运行库已安装
    echo.
    echo 已安装的 DLL:
    echo   ✅ vcruntime140.dll
    echo   ✅ msvcp140.dll
    echo.
    echo 无需修复
    echo.
    pause
    exit /b 0
)

echo ❌ 检测到缺失的 DLL:%MISSING_DLLS%
echo.
echo 这可能导致以下功能失败：
echo   • RapidOCR (图片文字识别)
echo   • PyMuPDF (PDF 文件处理)
echo   • NumPy/Pandas (数据处理)
echo.
echo 错误示例：
echo   ImportError: DLL load failed while importing core
echo   ImportError: cannot import name 'fitz'
echo.

REM ==================== 提供修复选项 ====================
echo ════════════════════════════════════════════════════
echo 修复选项:
echo ════════════════════════════════════════════════════
echo.
echo   1. 从本地安装包安装 (推荐)
echo   2. 从网络下载安装并安装
echo   3. 手动下载安装
echo   4. 退出
echo.

set /p choice="请选择操作 (1-4): "

if "%choice%"=="1" goto :install_local
if "%choice%"=="2" goto :install_online
if "%choice%"=="3" goto :install_manual
if "%choice%"=="4" goto :exit

echo 无效选项
pause
exit /b 1

:install_local
    echo.
    echo [选项 1] 从本地安装包安装
    echo.
    
    REM 检查多个可能的位置
    set "VCREDIST_PATH="
    
    if exist "%~dp0packages\vcredist_x64.exe" (
        set "VCREDIST_PATH=%~dp0packages\vcredist_x64.exe"
    ) else if exist "%~dp0..\packages\vcredist_x64.exe" (
        set "VCREDIST_PATH=%~dp0..\packages\vcredist_x64.exe"
    ) else if exist "%~dp0..\..\packages\vcredist_x64.exe" (
        set "VCREDIST_PATH=%~dp0..\..\packages\vcredist_x64.exe"
    )
    
    if "%VCREDIST_PATH%"=="" (
        echo ❌ 未找到本地安装包
        echo 请将 vcredist_x64.exe 放入 packages 目录
        echo.
        set /p retry="是否尝试网络下载？(Y/N): "
        if /i "%retry%"=="Y" goto :install_online
        goto :exit
    )
    
    echo 找到安装包：%VCREDIST_PATH%
    echo.
    echo 开始安装...
    echo.
    
    "%VCREDIST_PATH%" /install /quiet /norestart
    if errorlevel 1 (
        echo ⚠️  安装失败，错误代码：%errorlevel%
        echo 请尝试网络下载或手动安装
    ) else (
        echo ✅ 安装完成
    )
    
    goto :verify_install

:install_online
    echo.
    echo [选项 2] 从网络下载安装
    echo.
    echo 下载地址：%VCREDIST_URL%
    echo.
    echo 正在下载...
    
    powershell -Command "& {Invoke-WebRequest -Uri '%VCREDIST_URL%' -OutFile '%TEMP%\vcredist_x64.exe'}" 2>nul
    if errorlevel 1 (
        echo ❌ 下载失败
        echo 请检查网络连接或选择手动安装
        goto :install_manual
    )
    
    if not exist "%TEMP%\vcredist_x64.exe" (
        echo ❌ 下载失败，文件不存在
        goto :install_manual
    )
    
    echo ✅ 下载完成
    echo.
    echo 开始安装...
    echo.
    
    "%TEMP%\vcredist_x64.exe" /install /quiet /norestart
    if errorlevel 1 (
        echo ⚠️  安装失败，错误代码：%errorlevel%
    ) else (
        echo ✅ 安装完成
    )
    
    goto :verify_install

:install_manual
    echo.
    echo [选项 3] 手动安装
    echo.
    echo 请按以下步骤操作：
    echo.
    echo 1. 打开浏览器访问：
    echo    %VCREDIST_URL%
    echo.
    echo 2. 下载安装包 vc_redist.x64.exe
    echo.
    echo 3. 双击运行安装包
    echo.
    echo 4. 同意许可条款并安装
    echo.
    echo 5. 安装完成后重启此工具验证
    echo.
    
    set /p open_url="是否打开下载页面？(Y/N): "
    if /i "%open_url%"=="Y" (
        start %VCREDIST_URL%
    )
    
    goto :exit

:verify_install
    echo.
    echo ════════════════════════════════════════════════════
    echo 验证安装...
    echo ════════════════════════════════════════════════════
    echo.
    
    timeout /t 3 /nobreak >nul
    
    set "STILL_MISSING="
    
    if not exist "C:\Windows\System32\vcruntime140.dll" (
        set "STILL_MISSING=%STILL_MISSING% vcruntime140.dll"
    )
    
    if not exist "C:\Windows\System32\msvcp140.dll" (
        set "STILL_MISSING=%STILL_MISSING% msvcp140.dll"
    )
    
    if "%STILL_MISSING%"=="" (
        echo ✅ 验证成功！所有 DLL 已安装
        echo.
        echo ⚠️  建议：重启系统以确保所有程序能正确加载新 DLL
        echo.
        set /p restart="是否立即重启？(Y/N): "
        if /i "%restart%"=="Y" (
            shutdown /r /t 0
        )
    ) else (
        echo ⚠️  仍有缺失的 DLL:%STILL_MISSING%
        echo.
        echo 可能需要重启系统才能生效
        echo.
        set /p restart="是否立即重启？(Y/N): "
        if /i "%restart%"=="Y" (
            shutdown /r /t 0
        )
    )
    
    goto :exit

:exit
    echo.
    pause
    exit /b 0
