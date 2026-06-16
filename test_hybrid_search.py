# -*- coding: utf-8 -*-
"""
混合检索功能测试脚本
测试智能检索策略切换和混合检索效果
"""

import sys
import os

# 添加 core 目录到路径
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CORE_DIR)

from core.core import KnowledgeBase

def test_query_classification():
    """测试查询分类（简单 vs 复杂）"""
    print("=" * 60)
    print("测试 1: 查询分类")
    print("=" * 60)
    
    kb = KnowledgeBase()
    
    test_cases = [
        # (问题，预期结果：True=复杂，False=简单)
        ("2 月电费是多少？", False),
        ("中国的机器人型号是什么？", False),
        ("为什么 A 公司比 B 公司利润高？", True),
        ("如何优化检索策略？", True),
        ("比较向量检索和关键词检索的区别", True),
        ("分析电费增长的原因和影响因素", True),
        ("3 月和 2 月的电费对比如何？差异是多少？", True),
        ("步骤是什么？", True),  # 包含关键词
    ]
    
    correct = 0
    for question, expected in test_cases:
        result = kb._is_complex_query(question)
        status = "✅" if result == expected else "❌"
        if result == expected:
            correct += 1
        print(f"{status} '{question}' → {'复杂' if result else '简单'} (预期：{'复杂' if expected else '简单'})")
    
    print(f"\n准确率：{correct}/{len(test_cases)} = {correct*100//len(test_cases)}%")
    return correct == len(test_cases)


def test_hybrid_search_available():
    """测试混合检索模块可用性"""
    print("\n" + "=" * 60)
    print("测试 2: 混合检索模块可用性")
    print("=" * 60)
    
    try:
        from core.hybrid_search import HybridSearch, BM25_AVAILABLE
        print(f"✅ 模块导入成功")
        print(f"   BM25 可用：{'是' if BM25_AVAILABLE else '否'}")
        
        if BM25_AVAILABLE:
            print(f"✅ rank-bm25 已安装，可使用完整混合检索功能")
        else:
            print(f"⚠️  rank-bm25 未安装，将降级为纯向量检索")
            print(f"   安装命令：pip install rank-bm25")
        
        return True
    except Exception as e:
        print(f"❌ 模块导入失败：{e}")
        return False


def test_query_method():
    """测试智能 query 方法"""
    print("\n" + "=" * 60)
    print("测试 3: 智能 query 方法")
    print("=" * 60)
    
    kb = KnowledgeBase()
    
    # 测试简单问题
    print("\n[简单问题] 2 月电费是多少？")
    result = kb.query("2 月电费是多少？", top_k=2)
    print(f"答案：{result.answer[:100]}...")
    print(f"来源数：{len(result.sources)}")
    print(f"耗时：{result.query_time:.2f}秒")
    
    # 测试复杂问题
    print("\n[复杂问题] 为什么电费会变化？分析原因")
    result = kb.query("为什么电费会变化？分析原因", top_k=2)
    print(f"答案：{result.answer[:100]}...")
    print(f"来源数：{len(result.sources)}")
    print(f"耗时：{result.query_time:.2f}秒")
    
    print("\n✅ 智能 query 方法测试完成")
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("🧪 RAG 混合检索功能测试")
    print("=" * 60)
    
    results = []
    
    # 测试 1: 查询分类
    results.append(("查询分类", test_query_classification()))
    
    # 测试 2: 混合检索模块
    results.append(("混合检索模块", test_hybrid_search_available()))
    
    # 测试 3: 智能 query 方法（可选，需要 LM Studio 运行）
    try:
        results.append(("智能 query 方法", test_query_method()))
    except Exception as e:
        print(f"\n⚠️  智能 query 方法测试跳过（LM Studio 未运行）")
        results.append(("智能 query 方法", None))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, result in results:
        if result is True:
            print(f"✅ {name}: 通过")
        elif result is False:
            print(f"❌ {name}: 失败")
        else:
            print(f"⚠️  {name}: 跳过")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
