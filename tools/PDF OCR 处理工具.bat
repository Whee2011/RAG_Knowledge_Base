@echo off
chcp 65001 >nul
title PDF OCR 处理工具
cd /d "%~dp0"

echo ============================================================
echo PDF OCR 处理工具
echo ============================================================
echo.
echo 检查依赖库...
python -c "from rapidocr import RapidOCR; print('✅ RapidOCR 已安装')" 2>nul
if errorlevel 1 (
    echo ❌ RapidOCR 未安装
    echo.
    echo 正在安装依赖库...
    pip install rapidocr onnxruntime pymupdf pillow
    if errorlevel 1 (
        echo.
        echo ❌ 安装失败，请手动安装：
        echo    pip install rapidocr onnxruntime pymupdf pillow
        pause
        exit /b 1
    )
)
echo.

echo ============================================================
echo 请选择处理模式：
echo   1. 处理单个 PDF 文件
echo   2. 批量处理目录中的所有 PDF
echo ============================================================
echo.
set /p mode="请输入选项 (1 或 2): "

if "%mode%"=="1" (
    set /p filepath="请输入 PDF 文件路径："
    python ocr_processor.py "%filepath%"
) else if "%mode%"=="2" (
    set /p dirpath="请输入 PDF 目录路径："
    set /p outpath="请输入输出目录路径（可选，直接回车使用默认）: "
    if "%outpath%"=="" (
        python ocr_processor.py "%dirpath%"
    ) else (
        python ocr_processor.py "%dirpath%" "%outpath%"
    )
) else (
    echo ❌ 无效选项
)

echo.
pause
