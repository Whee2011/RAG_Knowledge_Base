# -*- coding: utf-8 -*-
"""测试 OCR - 使用 batch 模式"""
import os
import sys
import tempfile
import shutil

os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'
os.environ['FLAGS_use_parallel_program'] = '0'

sys.path.insert(0, '.')

from paddleocr import PaddleOCR
import pymupdf

print("Initializing OCR (batch mode)...")
ocr = PaddleOCR(
    use_textline_orientation=True,
    lang='ch',
    batch_size=1
)
print("OCR initialized.")

# 动态路径：脚本位于 tools/，项目根目录为父目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.dirname(SCRIPT_DIR)
PDF_DIR = os.path.join(INSTALL_DIR, "documents", "pdf")

# 测试梅西.pdf
pdf_path = os.path.join(PDF_DIR, "梅西.pdf")
print(f"\nProcessing: {os.path.basename(pdf_path)}")

# 检查是否需要 OCR
doc = pymupdf.open(pdf_path)
text = doc[0].get_text()
doc.close()

if text.strip() and len(text.strip()) > 50:
    print("This is a text PDF.")
    sys.exit(0)

print("This is an image PDF. Performing OCR...")

# PDF 转图片
temp_dir = tempfile.mkdtemp(prefix='ocr_')
doc = pymupdf.open(pdf_path)

print(f"Converting {len(doc)} pages to images...")
for i, page in enumerate(doc):
    mat = pymupdf.Matrix(200/72, 200/72)
    pix = page.get_pixmap(matrix=mat)
    img_path = os.path.join(temp_dir, f"page_{i:03d}.png")
    pix.save(img_path)

doc.close()

# OCR 识别
print("Performing OCR (this may take a while)...")
all_text = []

try:
    # 使用目录批量处理
    result = ocr.predict(temp_dir)
    
    if result and 'rec_texts' in result:
        texts = result.get('rec_texts', [])
        all_text.append("\n".join(texts))
        print(f"Recognized {len(texts)} text lines.")
except Exception as e:
    print(f"Error during OCR: {e}")
    print("Trying single image mode...")
    
    # 单张图片处理
    for i in range(min(3, len(os.listdir(temp_dir)))):
        img_path = os.path.join(temp_dir, f"page_{i:03d}.png")
        try:
            result = ocr.predict(img_path)
            if result and 'rec_texts' in result:
                texts = result.get('rec_texts', [])
                all_text.append(f"=== Page {i+1} ===\n" + "\n".join(texts))
                print(f"  Page {i+1}: {len(texts)} lines")
        except Exception as e2:
            print(f"  Page {i+1} failed: {e2}")

# 保存结果
if all_text:
    output_path = pdf_path.replace('.pdf', '_ocr.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(all_text))
    
    print(f"\nOCR completed!")
    print(f"Output: {output_path}")
    print(f"Total characters: {sum(len(t) for t in all_text)}")
else:
    print("\nNo text recognized.")

# 清理
shutil.rmtree(temp_dir, ignore_errors=True)
