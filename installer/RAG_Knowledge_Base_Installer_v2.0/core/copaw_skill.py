"""
RAG Knowledge Base Skill for CoPaw
本地知识库检索技能
"""
import sys
import os

# 动态路径：脚本位于 core/，项目根目录为父目录
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.dirname(CORE_DIR)
DEFAULT_DOCUMENTS_PATH = os.path.join(INSTALL_DIR, "documents")

sys.path.insert(0, CORE_DIR)

from core import KnowledgeBase
from datetime import datetime
from typing import List, Dict, Optional


def _get_kb(kb_name: str = "default") -> KnowledgeBase:
    """获取知识库实例"""
    # 优先使用与 copaw_skill.py 同项目的 documents 目录
    possible_paths = [DEFAULT_DOCUMENTS_PATH]

    # 兼容旧版硬编码路径（如果用户仍未迁移）
    legacy_paths = [
        r"D:\RAG_Knowledge_Base\documents",
        r"H:\RAG_Knowledge_Base\documents",
        r"C:\Users\Administrator\.copaw\workspaces\default\test_docs"
    ]

    for path in possible_paths + legacy_paths:
        if os.path.exists(path):
            return KnowledgeBase(
                name=kb_name,
                documents_path=path
            )

    # 默认使用动态推导路径
    return KnowledgeBase(
        name=kb_name,
        documents_path=DEFAULT_DOCUMENTS_PATH
    )


def rag_query(question: str, show_sources: bool = True, top_k: int = 5, kb_name: str = "default") -> str:
    """
    查询知识库
    
    Args:
        question: 要查询的问题
        show_sources: 是否显示来源文档
        top_k: 检索的文档数量
        kb_name: 知识库名称
    
    Returns:
        格式化的答案字符串
    """
    try:
        kb = _get_kb(kb_name)
        result = kb.query_with_sources(question, top_k=top_k)
        
        output = f"📚 **答案：**\n\n{result.answer}\n"
        
        if show_sources and result.sources:
            output += "\n📄 **来源：**\n"
            # 去重
            seen = set()
            for s in result.sources:
                source_key = s['source']
                if source_key not in seen:
                    seen.add(source_key)
                    output += f"  • [{s['index']}] {s['source']}\n"
        
        return output
    
    except Exception as e:
        return f"❌ 查询失败：{str(e)}"


def rag_status(kb_name: str = "default") -> str:
    """
    查看知识库状态
    
    Args:
        kb_name: 知识库名称
    
    Returns:
        格式化的状态信息
    """
    try:
        kb = _get_kb(kb_name)
        status = kb.get_status()
        
        output = f"📊 **知识库状态 ({kb_name})**\n"
        output += "━" * 30 + "\n"
        output += f"📄 文档数量：{status.total_documents}\n"
        output += f"📦 文本块数：{status.total_chunks}\n"
        output += f"🕐 最后更新：{status.last_updated}\n"
        
        if status.documents:
            output += "\n**文档列表:**\n"
            for doc in status.documents:
                output += f"  • {doc['path']} ({doc['chunks']} 块)\n"
        
        return output
    
    except Exception as e:
        return f"❌ 获取状态失败：{str(e)}"


def rag_refresh(kb_name: str = "default", force: bool = False, auto_ocr: bool = True) -> str:
    """
    刷新知识库索引（自动检测并处理 OCR）
    
    Args:
        kb_name: 知识库名称
        force: 是否强制重建索引
        auto_ocr: 是否自动检测并处理需要 OCR 的文件（默认 True）
    
    Returns:
        刷新结果
    """
    try:
        kb = _get_kb(kb_name)
        kb.add_documents(force=force, auto_ocr=auto_ocr)
        status = kb.get_status()
        
        if force:
            output = "🔄 **索引已重建**\n"
        else:
            output = "✅ **索引已更新**\n"
        
        output += f"  📄 文档数量：{status.total_documents}\n"
        output += f"  📦 文本块数：{status.total_chunks}\n"
        output += f"  🕐 更新时间：{status.last_updated}\n"
        
        if auto_ocr:
            output += f"\n💡 **自动 OCR 已启用** - 新放入的图片 PDF 将自动识别\n"
        
        return output
    
    except Exception as e:
        return f"❌ 刷新失败：{str(e)}"


def rag_extract(question: str, fields: List[str], kb_name: str = "default") -> str:
    """
    从 Excel/CSV 文档中提取结构化数据

    Args:
        question: 问题描述，例如"2025年销售额总和是多少？"
        fields: 要提取的字段列表（可选提示）
        kb_name: 知识库名称

    Returns:
        格式化的提取结果
    """
    try:
        kb = _get_kb(kb_name)
        result = kb.extract_data(question, fields=fields)

        if 'error' in result and not result.get('answer'):
            return f"❌ 提取失败：{result['error']}"

        output = f"📊 **提取结果：**\n\n"
        output += result.get('answer', '未找到相关数据')

        # 如果指定了字段且有提取结果，显示字段表格
        extracted = result.get('extracted_fields')
        if fields and extracted:
            output += "\n\n**字段提取：**\n"
            output += "| " + " | ".join(fields) + " |\n"
            output += "|" + "|".join(["------" for _ in fields]) + "|\n"
            for row in extracted[:10]:
                values = [str(row.get(f, "-")) for f in fields]
                output += "| " + " | ".join(values) + " |\n"

        output += f"\n\n数据来源：{kb_name} 知识库"

        return output

    except Exception as e:
        return f"❌ 提取失败：{str(e)}"


def rag_list_documents(kb_name: str = "default") -> str:
    """
    列出知识库中的所有文档
    
    Args:
        kb_name: 知识库名称
    
    Returns:
        文档列表
    """
    try:
        kb = _get_kb(kb_name)
        status = kb.get_status()
        
        if not status.documents:
            return "📭 知识库中暂无文档"
        
        output = f"📚 **知识库文档列表 ({kb_name})**\n"
        output += "━" * 30 + "\n"
        
        for i, doc in enumerate(status.documents, 1):
            output += f"{i}. **{doc['path']}**\n"
            output += f"   文本块：{doc['chunks']} | 添加时间：{doc.get('added_at', '未知')[:19]}\n"
        
        return output
    
    except Exception as e:
        return f"❌ 获取文档列表失败：{str(e)}"


def rag_search_by_keyword(keyword: str, top_k: int = 10, kb_name: str = "default") -> str:
    """
    按关键词搜索文档片段
    
    Args:
        keyword: 搜索关键词
        top_k: 返回结果数量
        kb_name: 知识库名称
    
    Returns:
        搜索结果
    """
    try:
        kb = _get_kb(kb_name)
        kb.add_documents()  # 确保索引最新
        
        # 使用语义搜索
        docs = kb.vectorstore.similarity_search(keyword, k=top_k)
        
        if not docs:
            return f"🔍 未找到与 \"{keyword}\" 相关的内容"
        
        output = f"🔍 **搜索结果：\"{keyword}\"**\n"
        output += f"找到 {len(docs)} 个相关片段\n\n"
        
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', '未知')
            content = doc.page_content[:300].replace('\n', ' ')
            output += f"**[{i}] 来源：** {source}\n"
            output += f"**内容：** {content}...\n\n"
            output += "─" * 30 + "\n"
        
        return output
    
    except Exception as e:
        return f"❌ 搜索失败：{str(e)}"


# 技能元数据
SKILL_INFO = {
    "name": "rag_knowledge",
    "version": "1.0.0",
    "description": "本地知识库智能检索技能",
    "author": "CoPaw Assistant",
    "functions": [
        "rag_query",
        "rag_status", 
        "rag_refresh",
        "rag_extract",
        "rag_list_documents",
        "rag_search_by_keyword"
    ],
    "triggers": [
        "查一下知识库",
        "检索文档",
        "根据文档",
        "知识库中",
        "RAG 检索",
        "知识库状态",
        "刷新索引",
        "提取.*数据"
    ]
}


# 测试
if __name__ == "__main__":
    print("测试 RAG 技能...")
    print("\n" + "=" * 50)
    
    # 测试查询
    print("1. 测试查询：")
    print(rag_query("总部职责是什么？"))
    
    print("\n" + "=" * 50)
    
    # 测试状态
    print("2. 测试状态：")
    print(rag_status())
    
    print("\n" + "=" * 50)
    print("测试完成！")
