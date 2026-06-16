# -*- coding: utf-8 -*-
"""OCR 处理 - 简化版（基于 RapidOCR）"""
import os
import sys
import tempfile
import shutil

from rapidocr import RapidOCR
import pymupdf

def ocr_pdf(pdf_path, output_path=None):
    """对 PDF 进行 OCR"""
    
    print(f"Processing: {os.path.basename(pdf_path)}")
    
    # 检查是否需要 OCR
    try:
        doc = pymupdf.open(pdf_path)
        text = doc[0].get_text()
        doc.close()
        
        if text.strip() and len(text.strip()) > 50:
            print("This is a text PDF, skipping OCR.")
            return None
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    
    print("This is an image PDF. Converting to images...")
    
    # PDF 转图片
    temp_dir = tempfile.mkdtemp(prefix='ocr_')
    doc = pymupdf.open(pdf_path)
    image_paths = []
    
    for i, page in enumerate(doc):
        mat = pymupdf.Matrix(200/72, 200/72)
        pix = page.get_pixmap(matrix=mat)
        img_path = os.path.join(temp_dir, f"page_{i:03d}.png")
        pix.save(img_path)
        image_paths.append(img_path)
    
    doc.close()
    print(f"Converted {len(image_paths)} pages.")
    
    # OCR 识别
    print("Initializing OCR engine...")
    
    # 使用 wheel 包自带的 infer 模型（无需联网下载）
    import rapidocr
    models_dir = str(os.path.join(os.path.dirname(rapidocr.__file__), 'models'))
    params = {
        'Global.model_root_dir': models_dir,  # 必须显式设置，避免 WindowsPath 类型
        'Det.model_path': str(os.path.join(models_dir, 'ch_PP-OCRv4_det_infer.onnx')),
        'Rec.model_path': str(os.path.join(models_dir, 'ch_PP-OCRv4_rec_infer.onnx')),
        'Cls.model_path': str(os.path.join(models_dir, 'ch_ppocr_mobile_v2.0_cls_infer.onnx')),
    }
    ocr = RapidOCR(params=params)
    
    print("Performing OCR...")
    all_text = []
    
    for i, img_path in enumerate(image_paths):
        try:
            output = ocr(img_path)
            if output and output.txts:
                texts = output.txts
                all_text.append(f"=== Page {i+1} ===\n" + "\n".join(texts))
                print(f"  Page {i+1}: {len(texts)} lines")
        except Exception as e:
            print(f"  Page {i+1} error: {e}")
    
    # 保存结果
    if all_text:
        if output_path is None:
            output_path = pdf_path.replace('.pdf', '_ocr.txt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(all_text))
        
        print(f"\nCompleted!")
        print(f"Output: {os.path.basename(output_path)}")
        print(f"Total: {len(all_text)} pages, {sum(len(t) for t in all_text)} chars")
        
        shutil.rmtree(temp_dir, ignore_errors=True)
        return output_path
    else:
        print("No text recognized.")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ocr_simple.py <pdf_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)
    
    ocr_pdf(pdf_path)