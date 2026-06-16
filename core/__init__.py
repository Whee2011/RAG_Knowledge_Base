"""
RAG Knowledge Base Tool
老板的本地知识库检索工具
"""
from .core import KnowledgeBase
from .excel_analyzer import ExcelAnalyzer, format_excel_result

__version__ = "1.0.0"
__all__ = ["KnowledgeBase", "ExcelAnalyzer", "format_excel_result"]
