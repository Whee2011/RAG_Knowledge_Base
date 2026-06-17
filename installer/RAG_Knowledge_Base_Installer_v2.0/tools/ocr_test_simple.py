# -*- coding: utf-8 -*-
"""简化 OCR 测试"""
import os
import sys
import tempfile
import shutil

os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'
sys.path.insert(0, '.')

from paddleocr import PaddleOCR
import pymupdf

print("Initializing OCR...")
ocr = PaddleOCR(use_textline_orientation=True, lang='ch')
print("OCR initialized.")

# 动态路径：脚本位于 tools/，项目根目录为父目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.dirname(SCRIPT_DIR)
PDF_DIR = os.path.join(INSTALL_DIR, "documents", "pdf")

# 测试梅西.pdf
pdf_path = os.path.join(PDF_DIR, "梅西.pdf")
print(f"\nProcessing: {pdf_path}")

# 检查是否需要 OCR
doc = pymupdf.open(pdf_path)
text = doc[0].get_text()
doc.close()

if text.strip() and len(text.strip()) > 50:
    print("This is a text PDF, no OCR needed.")
    sys.exit(0)

print("This is an image PDF, performing OCR...")

# PDF 转图片
temp_dir = tempfile.mkdtemp(prefix='ocr_')
doc = pymupdf.open(pdf_path)
image_paths = []

print(f"Converting PDF to images ({len(doc)} pages)...")
for i, page in enumerate(doc):
    mat = pymupdf.Matrix(200/72, 200/72)
    pix = page.get_pixmap(matrix=mat)
    img_path = os.path.join(temp_dir, f"page_{i:03d}.png")
    pix.save(img_path)
    image_paths.append(img_path)

doc.close()
print(f"Converted {len(image_paths)} pages.")

# OCR 识别
print("Performing OCR...")
all_text = []

for i, img_path in enumerate(image_paths):
    result = ocr.predict(img_path)
    if result and 'rec_texts' in result:
        texts = result.get('rec_texts', [])
        all_text.append(f"=== Page {i+1} ===\n" + "\n".join(texts))
    
    if (i + 1) % 5 == 0:
        print(f"  Processed {i+1}/{len(image_paths)} pages...")

# 保存结果
output_path = pdf_path.replace('.pdf', '_ocr.txt')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_text))

# 清理
shutil.rmtree(temp_dir)

print(f"\nOCR completed!")
print(f"Output: {output_path}")
print(f"Total pages: {len(image_paths)}")
print(f"Total characters: {sum(len(t) for t in all_text)}")
