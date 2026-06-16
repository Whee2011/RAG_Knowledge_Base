@echo off
chcp 65001 >nul
title 安装 Tesseract OCR
cd /d "C:\Users\Administrator\.copaw\workspaces\default\rag_knowledge"
echo ============================================================
echo 安装 Tesseract OCR（替代方案）
echo ============================================================
echo.
echo Tesseract 是一个开源 OCR 引擎，由 Google 维护
echo.
echo 下载地址：
echo https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 1. 下载并安装 Tesseract 5 for Windows
echo 2. 安装时记住安装路径（默认：C:\Program Files\Tesseract-OCR）
echo 3. 安装完成后，重新运行此脚本
echo.
echo ============================================================
set /p installed="是否已安装 Tesseract? (y/n): "
if "%installed%"=="y" (
    set /p path="请输入 Tesseract 安装路径："
    setx TESSDATA_PREFIX "%path%\tessdata"
    echo.
    echo 正在安装 Python 绑定...
    pip install pytesseract pillow
    echo.
    echo 测试安装...
    python -c "import pytesseract; print('Tesseract path:', pytesseract.get_tesseract_version())"
    echo.
    echo 安装完成！
) else (
    echo.
    echo 请先下载安装 Tesseract
    echo 下载后重新运行此脚本
)
pause
