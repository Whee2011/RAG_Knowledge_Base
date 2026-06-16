@echo off
chcp 65001 >nul
title 安装 OCR 依赖（RapidOCR）
cd /d "C:\Users\Administrator\.copaw\workspaces\default\rag_knowledge"
echo ============================================================
echo 安装 PDF OCR 依赖库（基于 RapidOCR）
echo ============================================================
echo.
echo 正在安装...
echo.
echo 1. 安装 RapidOCR（OCR 引擎）
pip install rapidocr -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
echo 2. 安装 ONNX Runtime（推理引擎）
pip install onnxruntime -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
echo 3. 安装其他依赖
pip install pymupdf pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
echo ============================================================
echo 安装完成！
echo ============================================================
echo.
echo 测试安装...
python -c "from rapidocr import RapidOCR; ocr = RapidOCR(); print('✅ RapidOCR 安装成功')"
echo.
pause