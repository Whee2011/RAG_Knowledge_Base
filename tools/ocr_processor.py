# -*- coding: utf-8 -*-
"""
PDF OCR 处理模块
自动检测图片 PDF 并进行 OCR 识别
"""
import os
import sys
import tempfile
import shutil

# 检查并安装依赖
try:
    from paddleocr import PaddleOCR
    import pymupdf
    from PIL import Image
    import numpy as np
except ImportError as e:
    print("❌ 缺少依赖库，请先安装：")
    print("   pip install paddleocr paddlepaddle pymupdf pillow numpy")
    sys.exit(1)


class PDFOCR:
    """PDF OCR 处理器"""
    
    def __init__(self, lang='ch'):
        """
        初始化 OCR
        
        Args:
            lang: 识别语言 ('ch' 中文，'en' 英文，'japan' 日文等)
        """
        print("Initializing OCR engine...")
        import os
        os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'
        
        self.ocr = PaddleOCR(
            use_textline_orientation=True,
            lang=lang
        )
        print("OCR engine initialized.")
    
    def is_image_pdf(self, pdf_path: str) -> bool:
        """
        检测 PDF 是否是图片 PDF（无文字层）
        
        Returns:
            True: 图片 PDF，需要 OCR
            False: 文字 PDF，无需 OCR
        """
        try:
            doc = pymupdf.open(pdf_path)
            
            # 检查前 3 页
            check_pages = min(3, len(doc))
            has_text = False
            
            for i in range(check_pages):
                page = doc[i]
                text = page.get_text()
                if text.strip() and len(text.strip()) > 50:
                    has_text = True
                    break
            
            doc.close()
            
            if has_text:
                print(f"  ✅ 文字 PDF：{os.path.basename(pdf_path)}")
                return False
            else:
                print(f"  ⚠️  图片 PDF：{os.path.basename(pdf_path)}，需要 OCR")
                return True
                
        except Exception as e:
            print(f"  ❌ 检测失败：{e}")
            return False
    
    def pdf_to_images(self, pdf_path: str, temp_dir: str, dpi=200) -> list:
        """
        将 PDF 转换为图片
        
        Returns:
            图片路径列表
        """
        doc = pymupdf.open(pdf_path)
        image_paths = []
        
        print(f"  📸 转换 PDF 为图片（{len(doc)} 页）...")
        
        for i, page in enumerate(doc):
            # 渲染页面为图片
            mat = pymupdf.Matrix(dpi/72, dpi/72)
            pix = page.get_pixmap(matrix=mat)
            
            # 保存图片
            img_path = os.path.join(temp_dir, f"page_{i:03d}.png")
            pix.save(img_path)
            image_paths.append(img_path)
            
            if (i + 1) % 5 == 0:
                print(f"    已转换 {i+1}/{len(doc)} 页...")
        
        doc.close()
        return image_paths
    
    def ocr_image(self, image_path: str) -> str:
        """
        对单张图片进行 OCR
        
        Returns:
            识别的文字
        """
        # 使用新 API
        result = self.ocr.predict(image_path)
        
        if not result or 'rec_texts' not in result:
            return ""
        
        # 提取文字
        texts = result.get('rec_texts', [])
        confidences = result.get('rec_scores', [])
        
        # 过滤低置信度
        filtered_texts = []
        for text, conf in zip(texts, confidences):
            if conf > 0.5:
                filtered_texts.append(text)
        
        return "\n".join(filtered_texts)
    
    def ocr_pdf(self, pdf_path: str, output_path: str = None) -> str:
        """
        对 PDF 进行 OCR 识别
        
        Args:
            pdf_path: PDF 文件路径
            output_path: 输出文本文件路径（可选）
        
        Returns:
            输出文件路径
        """
        print(f"\n📚 开始 OCR 处理：{os.path.basename(pdf_path)}")
        
        # 1. 创建临时目录
        temp_dir = tempfile.mkdtemp(prefix='ocr_')
        
        try:
            # 2. PDF 转图片
            image_paths = self.pdf_to_images(pdf_path, temp_dir)
            
            # 3. OCR 识别
            print(f"  🔍 开始 OCR 识别（{len(image_paths)} 页）...")
            all_text = []
            
            for i, img_path in enumerate(image_paths):
                text = self.ocr_image(img_path)
                if text:
                    all_text.append(f"=== 第 {i+1} 页 ===\n{text}")
                
                if (i + 1) % 5 == 0:
                    print(f"    已识别 {i+1}/{len(image_paths)} 页...")
            
            # 4. 保存结果
            if not output_path:
                output_path = pdf_path.replace('.pdf', '_ocr.txt')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(all_text))
            
            print(f"\n✅ OCR 完成！")
            print(f"   输出文件：{output_path}")
            print(f"   总页数：{len(image_paths)}")
            print(f"   识别文字：{sum(len(t) for t in all_text)} 字符")
            
            return output_path
            
        finally:
            # 5. 清理临时文件
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def process_directory(self, dir_path: str, output_dir: str = None):
        """
        批量处理目录中的所有 PDF
        
        Args:
            dir_path: PDF 目录
            output_dir: 输出目录（可选）
        """
        print("=" * 60)
        print(f"批量 OCR 处理：{dir_path}")
        print("=" * 60)
        
        # 找到所有 PDF
        pdf_files = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.lower().endswith('.pdf') and not file.startswith('~$'):
                    pdf_files.append(os.path.join(root, file))
        
        print(f"\n找到 {len(pdf_files)} 个 PDF 文件")
        
        # 处理每个 PDF
        results = []
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}] ", end="")
            
            # 检测是否需要 OCR
            if not self.is_image_pdf(pdf_path):
                continue
            
            # 确定输出路径
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                filename = os.path.basename(pdf_path).replace('.pdf', '_ocr.txt')
                output_path = os.path.join(output_dir, filename)
            else:
                output_path = None
            
            # OCR 处理
            try:
                result_path = self.ocr_pdf(pdf_path, output_path)
                results.append((pdf_path, result_path, '成功'))
            except Exception as e:
                print(f"  ❌ 处理失败：{e}")
                results.append((pdf_path, None, f'失败：{e}'))
        
        # 显示结果
        print("\n" + "=" * 60)
        print("处理结果")
        print("=" * 60)
        for pdf_path, output_path, status in results:
            filename = os.path.basename(pdf_path)
            if output_path:
                print(f"✅ {filename} → {os.path.basename(output_path)}")
            else:
                print(f"⊘ {filename} (文字 PDF，跳过)")
        
        print("=" * 60)
        return results


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  python ocr_processor.py <PDF 文件路径>")
        print("  python ocr_processor.py <PDF 目录路径> [输出目录]")
        print("\n示例：")
        print("  python ocr_processor.py <INSTALL_DIR>\\documents\\pdf\\梅西.pdf")
        print("  python ocr_processor.py <INSTALL_DIR>\\documents\\pdf <INSTALL_DIR>\\documents\\txt")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 创建 OCR 处理器
    ocr = PDFOCR(lang='ch')
    
    # 处理文件或目录
    if os.path.isfile(input_path):
        # 单个文件
        if ocr.is_image_pdf(input_path):
            ocr.ocr_pdf(input_path)
        else:
            print("ℹ️  这是文字 PDF，无需 OCR")
    else:
        # 目录
        ocr.process_directory(input_path, output_dir)


if __name__ == "__main__":
    main()
