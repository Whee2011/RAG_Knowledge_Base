# 🔤 RAG 知识库 - OCR 功能使用指南

**版本：** v3.3  
**更新日期：** 2026-04-22  
**适合人群：** 所有用户

---

## 📖 本章内容

介绍 RAG 知识库的 OCR（光学字符识别）功能，用于识别图片 PDF 中的文字。

---

## 🎯 功能概述

### 什么是 OCR？

OCR（Optical Character Recognition）是一种将图片中的文字转换为可编辑文本的技术。

### 应用场景

- ✅ **图片 PDF** - 扫描版文档、电子书
- ✅ **Word 图片** - 文档中嵌入的图片
- ✅ **截图识别** - 包含文字的截图
- ✅ **表格图片** - 包含数据的表格图片

### 技术规格

| 项目 | 规格 |
|------|------|
| **OCR 引擎** | RapidOCR（基于 ONNX Runtime） |
| **模型** | PP-OCRv4（中文优化） |
| **支持语言** | 中文、英文、日文、韩文等 80+ |
| **识别准确率** | 95%+（打印文档） |
| **识别速度** | 2-5 秒/页 |
| **依赖版本** | RapidOCR 3.8.1 + ONNX Runtime 1.23.3 |
| **优势** | 无 protobuf/numpy 版本限制 |

---

## 🚀 快速使用

### 方式一：Web 界面（推荐）⭐

**步骤：**

1. 打开 Web 界面
   ```
   http://localhost:5000
   ```

2. 上传图片 PDF
   - 拖拽文件到上传区域
   - 或点击选择文件

3. 点击"OCR 处理"按钮

4. 等待处理完成
   - 自动生成 `[文件名]_ocr.txt`
   - 自动索引到知识库

5. 查询知识库
   - 输入相关问题
   - 获取答案和来源

---

### 方式二：交互式工具

**启动工具：**
```batch
# 双击启动
D:\RAG_Knowledge_Base\tools\PDF OCR 处理工具.bat
```

**操作步骤：**
```
╔════════════════════════════════════════════════════╗
║       PDF OCR 处理工具                             ║
╚════════════════════════════════════════════════════╝

请选择模式:
  1. 处理单个 PDF 文件
  2. 批量处理目录中的所有 PDF
  3. 退出

输入选项：1

请输入 PDF 文件路径：D:\documents\文件.pdf

正在识别...
✅ 识别完成
输出文件：D:\documents\文件_ocr.txt
```

---

### 方式三：命令行

**单个文件：**
```batch
python D:\RAG_Knowledge_Base\tools\ocr_simple.py "D:\documents\文件.pdf"
```

**批量处理：**
```batch
python D:\RAG_Knowledge_Base\tools\ocr_processor.py --batch "D:\documents"
```

---

### 方式四：Python API

```python
from tools.ocr_processor import PDFOCR

# 创建 OCR 实例
ocr = PDFOCR(lang='ch')

# 检测是否为图片 PDF
if ocr.is_image_pdf("文件.pdf"):
    print("这是图片 PDF，需要 OCR")
    
    # 执行 OCR
    ocr.ocr_pdf("文件.pdf", "输出.txt")
    print("OCR 完成")
else:
    print("这是文字 PDF，无需 OCR")
```

---

## 📋 详细功能

### 1. 自动 OCR

**功能：** 新文件放入时自动检测并 OCR

**配置：**
```yaml
# config.yaml
ocr:
  enable_ocr: true
  auto_ocr: true
  ocr_lang: "ch"
```

**工作流程：**
```
新文件放入 documents/
   ↓
检测是否为图片 PDF
   ↓
是 → 自动 OCR 识别
   ↓
生成 _ocr.txt 文件
   ↓
自动索引到知识库
```

---

### 2. 手动 OCR

**适用场景：**
- 自动 OCR 失败
- 选择性处理特定文件
- 重新 OCR（提高质量）

**操作步骤：**

#### Web 界面
1. 打开"文件管理"标签页
2. 找到目标文件
3. 点击"OCR"按钮
4. 等待处理完成

#### 命令行
```batch
python D:\RAG_Knowledge_Base\tools\ocr_simple.py "文件.pdf"
```

---

### 3. 批量 OCR

**适用场景：**
- 大量历史文档
- 整个目录的 PDF

**操作步骤：**

```batch
# 批量处理目录
python D:\RAG_Knowledge_Base\tools\ocr_processor.py --batch "D:\documents"

# 带参数
python D:\RAG_Knowledge_Base\tools\ocr_processor.py --batch "D:\documents" --lang ch
```

---

## 📊 OCR 输出

### 输出文件

**命名规则：**
```
原文件.pdf → 原文件_ocr.txt
```

**文件位置：**
```
与原 PDF 同一目录
```

**文件格式：**
```
页面 1
====
[识别的文字内容]

页面 2
====
[识别的文字内容]

...
```

### 示例

**输入：** `梅西.pdf`（12 页图片 PDF）

**输出：** `梅西_ocr.txt`
```
页面 1
====
里奥·梅西（Lionel Messi），1987 年 6 月 24 日出生，
阿根廷职业足球运动员...

页面 2
====
2004 年，梅西与巴塞罗那签订第一份职业合同...

...
```

---

## 🔧 高级功能

### Word 文档图片 OCR

**功能：** 提取 Word 文档中的图片并 OCR

**使用：**
```batch
# 自动处理
python D:\RAG_Knowledge_Base\tools\ocr_processor.py "文档.docx"
```

**流程：**
```
Word 文档
   ↓
提取所有图片
   ↓
逐张 OCR 识别
   ↓
合并输出文本
```

---

### 表格 OCR

**功能：** 识别表格图片中的数据和结构

**使用：**
```python
from tools.ocr_processor import PDFOCR

ocr = PDFOCR(lang='ch')
ocr.ocr_table("表格图片.png", "输出.txt")
```

---

## ⚙️ 配置选项

### OCR 配置

```yaml
ocr:
  # 是否启用 OCR
  enable_ocr: true
  
  # 是否自动 OCR
  auto_ocr: true
  
  # OCR 语言
  # ch: 中文
  # en: 英文
  # ja: 日文
  # ko: 韩文
  ocr_lang: "ch"
  
  # 模型路径（留空使用默认）
  ocr_model_path: ""
  
  # 识别置信度阈值
  ocr_threshold: 0.5
```

---

## 📈 性能指标

### 识别速度

| 文档类型 | 速度 | 说明 |
|---------|------|------|
| 文字 PDF | 无需 OCR | 直接提取 |
| 图片 PDF（1 页） | 2-5 秒 | 首次需下载模型 |
| 图片 PDF（10 页） | 20-50 秒 | 批量处理 |
| Word 图片 | 1-3 秒/张 | 取决于图片数量 |

### 识别准确率

| 文档类型 | 准确率 | 说明 |
|---------|--------|------|
| 打印文档 | 95%+ | 清晰印刷体 |
| 手写文档 | 60-80% | 取决于字迹 |
| 模糊文档 | 70-90% | 取决于清晰度 |
| 表格 | 90%+ | 规则表格 |

---

## 🔍 故障排查

### 问题 1：OCR 失败

**症状：**
```
❌ OCR 识别失败
❌ ImportError: No module named 'rapidocr'
```

**原因：**
- RapidOCR 未安装
- VC++ 运行库缺失

**解决：**
```batch
# 安装 RapidOCR
pip install rapidocr onnxruntime

# 安装 VC++
D:\RAG_Knowledge_Base\fix_vcredist.bat
```

---

### 问题 2：识别准确率低

**症状：**
- 识别结果错别字多
- 文字顺序混乱

**原因：**
- 图片质量差
- 字体特殊
- 倾斜角度大

**解决：**
1. 提高原图质量（重新扫描）
2. 调整图片（矫正倾斜）
3. 手动校对

---

### 问题 3：OCR 速度慢

**症状：**
- 单页超过 10 秒
- CPU 占用高

**原因：**
- 图片分辨率过高
- CPU 性能不足

**解决：**
1. 降低图片分辨率（建议 300 DPI）
2. 关闭其他程序
3. 升级硬件

---

## 📚 依赖说明

### 核心依赖

```requirements.txt
# OCR 引擎（替代 PaddleOCR）
rapidocr

# ONNX Runtime（推理引擎）
# onnxruntime（chromadb 已包含）

# 图片处理
pillow

# PDF 处理
pymupdf
```

### 版本要求

✅ **RapidOCR 优势：**
- 无 protobuf 版本限制（copaw 可正常启动）
- 无 numpy ABI 版本限制
- 使用相同的 PP-OCRv4 模型（识别质量不变）
- 离线安装更简单（包体积更小）

⚠️ **已移除的依赖：**
- `paddlepaddle`（与 copaw protobuf 冲突）
- `paddleocr`（依赖 protobuf ≤3.30.2）

---

## 🎯 最佳实践

### 1. 文档预处理

- 扫描分辨率：300 DPI
- 图片格式：PNG/JPG
- 文字方向：水平
- 背景：纯色最佳

### 2. 批量处理

```batch
# 夜间批量处理
python D:\RAG_Knowledge_Base\tools\ocr_processor.py --batch "D:\documents" --async
```

### 3. 质量检查

```python
# 检查 OCR 结果
with open("文件_ocr.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(f"识别字数：{len(content)}")
    
    # 检查是否有乱码
    if "" in content:
        print("警告：检测到乱码")
```

---

## 📋 使用场景示例

### 场景 1：扫描版合同

```
1. 扫描合同为 PDF
2. 放入 documents/目录
3. 自动 OCR 识别
4. 查询合同条款
```

### 场景 2：历史档案数字化

```
1. 批量扫描档案
2. 运行批量 OCR
3. 索引到知识库
4. 支持全文检索
```

### 场景 3：财务报表识别

```
1. 导出报表为 PDF
2. OCR 识别表格数据
3. 提取关键数据
4. 生成分析报告
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| [01-知识库使用说明.md](01-知识库使用说明.md) | 使用方式总览 |
| [24-命令速查表.md](24-命令速查表.md) | 常用命令 |
| [41-常见问题排查.md](41-常见问题排查.md) | 故障排查 |

---

**文档维护：** RAG 知识库团队  
**更新日期：** 2026-04-22  
**更新内容：** RapidOCR 替代 PaddleOCR（解决 protobuf 冲突）
