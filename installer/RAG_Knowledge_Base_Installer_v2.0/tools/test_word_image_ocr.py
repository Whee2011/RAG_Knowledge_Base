# -*- coding: utf-8 -*-
"""
测试 Word 文档图片 OCR 功能
"""

import sys
import os

# 动态路径：脚本位于 tools/，项目根目录为父目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.dirname(SCRIPT_DIR)
CORE_DIR = os.path.join(INSTALL_DIR, "core")
DOCUMENTS_PATH = os.path.join(INSTALL_DIR, "documents")

sys.path.insert(0, CORE_DIR)

from core import KnowledgeBase

def test_word_image_ocr():
    """测试 Word 图片 OCR 功能"""
    
    print("=" * 60)
    print("测试 Word 文档图片 OCR 功能")
    print("=" * 60)
    print()
    
    # 创建知识库实例
    kb = KnowledgeBase(documents_path=DOCUMENTS_PATH)

    # 测试 Word 文件路径
    test_word_path = os.path.join(DOCUMENTS_PATH, "docx", "测试图片.docx")
    
    if not os.path.exists(test_word_path):
        print(f"❌ 测试文件不存在：{test_word_path}")
        print()
        print("请将包含图片的 Word 文档放入以下目录：")
        print(f"  {os.path.dirname(test_word_path)}\\")
        print()
        print("然后重新运行测试")
        return
    
    print(f"测试文件：{test_word_path}")
    print()
    
    # 读取 Word 文档
    print("正在读取 Word 文档...")
    text = kb._load_docx(test_word_path)
    
    if text:
        print("\n✅ Word 文档读取成功！")
        print(f"\n提取的文本长度：{len(text)} 字符")
        
        # 检查是否有图片 OCR 内容
        if "[图片" in text and "内容]" in text:
            print("\n✅ 检测到图片 OCR 内容！")
            
            # 提取图片内容
            import re
            image_sections = re.findall(r'\[图片 \d+ 内容\](.*?)\[/图片内容\]', text, re.DOTALL)
            
            if image_sections:
                print(f"\n共识别 {len(image_sections)} 张图片")
                for i, img_text in enumerate(image_sections, 1):
                    print(f"\n--- 图片 {i} ---")
                    print(img_text.strip())
        else:
            print("\n⚠️  未检测到图片 OCR 内容")
            print("可能原因：")
            print("  1. Word 文档中没有图片")
            print("  2. 图片格式不支持")
            print("  3. OCR 识别失败")
        
        print("\n" + "=" * 60)
        print("前 500 字符预览：")
        print("=" * 60)
        print(text[:500])
        
    else:
        print("\n❌ Word 文档读取失败！")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_word_image_ocr()
