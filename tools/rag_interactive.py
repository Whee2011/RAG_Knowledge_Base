# -*- coding: utf-8 -*-
"""
RAG 知识库交互式管理工具
提供菜单式交互，方便管理知识库
"""

import sys
import os

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 动态路径：脚本位于 tools/，项目根目录为父目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.dirname(SCRIPT_DIR)
CORE_DIR = os.path.join(INSTALL_DIR, "core")
DOCUMENTS_PATH = os.path.join(INSTALL_DIR, "documents")

sys.path.insert(0, CORE_DIR)

from core import KnowledgeBase

# 全局知识库实例（只创建一次）
kb = None


def get_kb():
    """获取知识库实例（单例模式）"""
    global kb
    if kb is None:
        kb = KnowledgeBase(documents_path=DOCUMENTS_PATH)
    return kb


def print_header():
    """打印标题"""
    print("\n" + "=" * 60)
    print("        📚 RAG 知识库交互式管理工具")
    print("=" * 60)


def print_menu():
    """打印菜单"""
    print("\n请选择操作：")
    print("  1️⃣  刷新知识库索引")
    print("  2️⃣  提问查询")
    print("  3️⃣  检查知识库文档数量")
    print("  4️⃣  查看文档列表")
    print("  5️⃣  强制重建索引")
    print("  0️⃣  退出程序")
    print("-" * 60)


def refresh_index():
    """刷新知识库索引"""
    print("\n🔄 正在刷新知识库索引...")
    try:
        kb = get_kb()
        kb.add_documents()
        
        status = kb.get_status()
        print("\n✅ 刷新完成！")
        print(f"📊 当前状态:")
        print(f"   文档数：{status.total_documents}")
        print(f"   文本块数：{status.total_chunks}")
        print(f"   最后更新：{status.last_updated}")
    except Exception as e:
        print(f"\n❌ 刷新失败：{e}")
    
    input("\n按回车键继续...")


def ask_question():
    """提问查询"""
    print("\n🔍 请输入您的问题（输入 'q' 返回菜单）:")
    print("-" * 60)
    
    while True:
        question = input("\n您的问题：").strip()
        
        if question.lower() == 'q':
            break
        
        if not question:
            print("⚠️  问题不能为空，请重新输入")
            continue
        
        print("\n🤔 正在查询知识库...")
        try:
            kb = get_kb()
            result = kb.query_with_sources(question, top_k=5, auto_refresh=False)
            
            print("\n" + "=" * 60)
            print("📚 答案：")
            print("=" * 60)
            print(result.answer)
            
            if result.sources:
                print("\n📄 来源文档：")
                seen = set()
                for s in result.sources:
                    source_key = s['source']
                    if source_key not in seen:
                        seen.add(source_key)
                        print(f"  [{s['index']}] {s['source']}")
            
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ 查询失败：{e}")
        
        print("\n继续提问或输入 'q' 返回菜单")
    
    input("\n按回车键继续...")


def check_status():
    """检查知识库状态"""
    print("\n📊 正在检查知识库状态...")
    try:
        kb = KnowledgeBase(documents_path=DOCUMENTS_PATH)
        status = kb.get_status()
        
        print("\n" + "=" * 60)
        print("📊 知识库状态")
        print("=" * 60)
        print(f"📄 文档数量：{status.total_documents}")
        print(f"📦 文本块数：{status.total_chunks}")
        print(f"🕐 最后更新：{status.last_updated if status.last_updated else '从未更新'}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 获取状态失败：{e}")
    
    input("\n按回车键继续...")


def show_document_list():
    """显示文档列表"""
    print("\n📋 正在获取文档列表...")
    try:
        kb = KnowledgeBase(documents_path=DOCUMENTS_PATH)
        status = kb.get_status()
        
        print("\n" + "=" * 60)
        print(f"📋 文档列表（共 {status.total_documents} 个）")
        print("=" * 60)
        
        if status.documents:
            for i, doc in enumerate(status.documents, 1):
                filename = os.path.basename(doc['path'])
                chunks = doc['chunks']
                print(f"  {i}. {filename} ({chunks} 个文本块)")
        else:
            print("  暂无文档")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 获取文档列表失败：{e}")
    
    input("\n按回车键继续...")


def force_rebuild():
    """强制重建索引"""
    print("\n⚠️  警告：此操作将删除现有索引并重新创建！")
    confirm = input("确认要强制重建索引吗？(y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ 已取消操作")
        input("\n按回车键继续...")
        return
    
    import shutil
    
    index_path = os.path.join(DOCUMENTS_PATH, ".rag")
    
    try:
        # 删除旧索引
        if os.path.exists(index_path):
            print("🗑️  正在删除旧索引...")
            shutil.rmtree(index_path)
            print("✅ 旧索引已删除")
        
        # 创建新索引
        print("📚 正在创建新索引...")
        kb = KnowledgeBase(documents_path=DOCUMENTS_PATH)
        kb.add_documents()
        
        status = kb.get_status()
        print("\n✅ 重建完成！")
        print(f"📊 新状态:")
        print(f"   文档数：{status.total_documents}")
        print(f"   文本块数：{status.total_chunks}")
        
    except Exception as e:
        print(f"\n❌ 重建失败：{e}")
    
    input("\n按回车键继续...")


def main():
    """主函数"""
    print_header()
    
    # 初始化检查
    print("\n🔧 正在初始化...")
    try:
        kb = KnowledgeBase(documents_path=DOCUMENTS_PATH)
        status = kb.get_status()
        print(f"✅ 知识库加载成功")
        print(f"   当前文档数：{status.total_documents}")
        print(f"   当前文本块数：{status.total_chunks}")
    except Exception as e:
        print(f"⚠️  知识库加载失败：{e}")
    
    # 主循环
    while True:
        print_menu()
        
        choice = input("请输入选项 (0-5): ").strip()
        
        if choice == '1':
            refresh_index()
        elif choice == '2':
            ask_question()
        elif choice == '3':
            check_status()
        elif choice == '4':
            show_document_list()
        elif choice == '5':
            force_rebuild()
        elif choice == '0':
            print("\n👋 感谢使用，再见！")
            break
        else:
            print("\n❌ 无效选项，请输入 0-5 之间的数字")
            input("按回车键继续...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已中断")
    except Exception as e:
        print(f"\n❌ 程序错误：{e}")
        input("按回车键退出...")
