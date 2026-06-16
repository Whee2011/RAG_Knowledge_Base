# -*- coding: utf-8 -*-
"""
OCR 处理图片 PDF
将扫描件/图片 PDF 转换为可搜索的文本
"""
import sys
sys.path.insert(0, r"C:\Users\Administrator\.copaw\workspaces\default")

import pymupdf

# 注意：需要安装 paddleocr 或 pytesseract
# pip install paddleocr paddlepaddle
# 或
# pip install pytesseract pillow

def ocr_pdf(input_path, output_path):
    """对 PDF 进行 OCR 识别"""
    print(f"正在处理：{input_path}")
    
    doc = pymupdf.open(input_path)
    all_text = []
    
    for i, page in enumerate(doc):
        print(f"  处理第 {i+1}/{len(doc)} 页...")
        
        # 方法 1：尝试提取文字（如果有）
        text = page.get_text()
        if text.strip():
            all_text.append(f"=== 第 {i+1} 页 ===\n{text}")
        else:
            # 方法 2：使用 OCR（需要安装 OCR 库）
            print(f"    第 {i+1} 页无文字，需要 OCR...")
            # 这里可以添加 OCR 代码
            # 例如使用 paddleocr 或 pytesseract
    
    # 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(all_text))
    
    print(f"✅ 已保存到：{output_path}")
    return output_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        output_path = pdf_path.replace('.pdf', '_ocr.txt')
        ocr_pdf(pdf_path, output_path)
    else:
        print("用法：python ocr_pdf.py <PDF 文件路径>")
        print("示例：python ocr_pdf.py <INSTALL_DIR>\\documents\\pdf\\梅西.pdf")
