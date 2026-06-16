@echo off
chcp 65001 >nul
title RAG 知识库诊断工具
cd /d "%~dp0"

set "TOOLS_DIR=%~dp0"
set "TOOLS_DIR=%TOOLS_DIR:~0,-1%"
set "INSTALL_DIR=%TOOLS_DIR%\.."
set "DOCUMENTS_DIR=%INSTALL_DIR%\documents"

echo ============================================================
echo RAG 知识库诊断工具
echo ============================================================
echo.

echo [1/4] 检查 Python...
python --version
if errorlevel 1 (
    echo ❌ Python 未安装或不在 PATH 中
    pause
    exit /b 1
)
echo ✅ Python 正常
echo.

echo [2/4] 检查 LM Studio 连接...
python -c "import requests; r=requests.get('http://127.0.0.1:1234', timeout=5); print('✅ LM Studio 正常')" 2>nul
if errorlevel 1 (
    echo ❌ LM Studio 未运行或无法连接
    echo    请启动 LM Studio 并加载模型
    pause
    exit /b 1
)
echo.

echo [3/4] 检查知识库索引...
dir "%DOCUMENTS_DIR%\.rag\chroma_db" >nul 2>nul
if errorlevel 1 (
    echo ❌ 索引目录不存在
    echo    需要重建索引
    pause
    exit /b 1
)
echo ✅ 索引目录存在
echo.

echo [4/4] 测试查询...
python -c "import sys; sys.path.insert(0, r'%INSTALL_DIR%\core'); from core import KnowledgeBase; kb = KnowledgeBase(documents_path=r'%DOCUMENTS_DIR%'); r = kb.query_with_sources('散热系统集成的厂商有哪些', top_k=3); print('答案:', r.answer[:200])"
echo.

echo ============================================================
echo 诊断完成！
echo ============================================================
pause
