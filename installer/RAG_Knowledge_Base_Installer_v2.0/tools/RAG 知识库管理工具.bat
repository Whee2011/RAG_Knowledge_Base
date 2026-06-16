@echo off
chcp 65001 >nul
title RAG 知识库交互式管理工具
cd /d "%~dp0"
python rag_interactive.py
pause
