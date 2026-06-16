# 📦 RAG 知识库安装包 v3.3

**版本：** v3.3  
**发布日期：** 2026-04-22  
**Python 版本：** 3.11.9  
**依赖包版本：** cp311（Python 3.11 专用）  
**状态：** ✅ 生产就绪

---

## 🎯 安装包概述

本安装包包含完整的 RAG 知识库系统，支持：

- ✅ **离线安装** - 所有依赖包已预下载
- ✅ **一键安装** - 双击 install.bat 自动完成
- ✅ **版本锁定** - 所有依赖版本已测试验证
- ✅ **完整文档** - 15+ 个使用说明文档
- ✅ **Web 界面** - 浏览器操作界面
- ✅ **CoPaw 技能** - 可直接在 CoPaw 中调用
- ✅ **API Key 认证** - 支持 LM Studio API Key 认证

---

## 📦 安装包结构

```
RAG_Knowledge_Base_Installer_v2.0/
│
├── 📄 install.bat                    # 主安装脚本（双击运行）
├── 📄 requirements.txt               # Python 依赖列表
├── 📄 config.yaml.template           # 配置文件模板
├── 📄 check_environment.bat          # 环境检测工具
├── 📄 start_all.bat                  # 启动所有服务
├── 📄 stop_all.bat                   # 停止所有服务
├── 📄 status.bat                     # 查看服务状态
├── 📄 fix_vcredist.bat               # 修复 VC++ 运行库
├── 📄 download_packages.bat          # 下载依赖包（备用）
│
├── 📁 core/                          # 核心代码
│   ├── core.py                       # KnowledgeBase 核心类
│   ├── copaw_skill.py                # CoPaw 技能封装
│   ├── __init__.py                   # 包初始化
│   └── SKILL.md                      # 核心代码说明
│
├── 📁 tools/                         # 工具脚本
│   ├── rag_interactive.py            # 交互式管理工具
│   ├── rag_qa.py                     # 快速问答工具
│   ├── ocr_processor.py              # OCR 处理核心
│   ├── ocr_simple.py                 # 简化版 OCR
│   ├── ocr_pdf.py                    # PDF OCR 工具
│   ├── RAG 知识库管理工具.bat          # 交互式管理（双击）
│   ├── PDF OCR 处理工具.bat            # OCR 处理（双击）
│   ├── RAG 诊断工具.bat                # 系统诊断（双击）
│   ├── 安装 OCR 依赖.bat                # 安装 OCR 依赖
│   └── 安装 Tesseract OCR.bat           # 备选 OCR 方案
│
├── 📁 web/                           # Web 界面
│   ├── web_app.py                    # Flask Web 应用
│   ├── 启动 Web 界面.bat                # Web 启动脚本（双击）
│   └── templates/
│       └── index.html                # Web 界面 HTML
│
├── 📁 docs/                          # 使用文档
│   ├── 00-文档目录.md                 # 文档导航
│   ├── 01-知识库使用说明.md           # 基础使用
│   ├── 10-系统架构说明.md             # 架构设计
│   ├── 24-命令速查表.md               # 命令参考
│   ├── 30-OCR 功能使用指南.md          # OCR 使用
│   ├── 40-系统状态检查.md             # 状态检查
│   ├── 41-常见问题排查.md             # 问题排查
│   └── 50-Skill 技能说明.md            # CoPaw 技能
│
├── 📁 packages/                      # 预下载依赖包（离线安装用）
│   ├── python_embedded_311.zip       # Python 3.11.9 嵌入式环境
│   ├── vcredist_x64.exe             # Visual C++ 运行库
│   ├── requirements_cp311/           # Python 3.11 专用 whl 包
│   └── requirements_rag.txt          # 核心依赖列表
│
└── 📁 templates/                     # 模板文件
    └── documents/                    # 示例文档目录结构
```

---

## 🚀 快速开始

### 方式一：标准安装（推荐）

**步骤 1：下载安装包**

将 `RAG_Knowledge_Base_Installer_v2.0` 文件夹复制到目标电脑

**步骤 2：运行安装脚本**

```batch
# 右键点击 install.bat，选择"以管理员身份运行"
```

**步骤 3：按照提示操作**

1. 选择安装路径（推荐 D 盘）
2. 确认安装选项
3. 等待安装完成
4. 安装完成后重启电脑（如提示）

**步骤 4：启动系统**

```batch
# 方式 A：启动 Web 界面（推荐）
cd D:\RAG_Knowledge_Base\web
启动 Web 界面.bat

# 方式 B：使用交互式工具
cd D:\RAG_Knowledge_Base\tools
RAG 知识库管理工具.bat

# 方式 C：使用 CoPaw 技能
# 在 CoPaw 中直接提问："查一下知识库..."
```

---

### 方式二：手动安装（高级用户）

**前提条件：**
- Python 3.11.x 已安装
- Visual C++ 2015-2022 运行库已安装

**步骤 1：复制文件**

```batch
# 将整个安装包复制到目标目录
xcopy /E /I RAG_Knowledge_Base_Installer_v2.0 D:\RAG_Knowledge_Base
```

**步骤 2：安装依赖**

```batch
cd D:\RAG_Knowledge_Base

# 使用清华镜像源加速安装
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**步骤 3：验证安装**

```bash
python -c "import chromadb; import flask; import pymupdf; import paddleocr; print('✅ 所有依赖正常')"
```

**步骤 4：配置 LM Studio**

1. 下载并安装 LM Studio：https://lmstudio.ai/
2. 下载模型：
   - LLM: `qwen/qwen3.5-9b`
   - Embedding: `text-embedding-qwen3-embedding-4b`
3. 启动本地服务器（端口 1234）
4. **API Key 配置**（如果 LM Studio 开启了认证）：
   ```bash
   # 编辑 config/.env 文件
   # 将 API_KEY 设置为实际的 Key
   API_KEY=your-actual-api-key-here
   
   # 如果 LM Studio 未开启认证，保持默认即可
   API_KEY=your-api-key-here
   ```

**步骤 5：启动系统**

```batch
cd D:\RAG_Knowledge_Base\web
启动 Web 界面.bat
```

---

## 📋 系统要求

### 最低配置

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 10 64 位 |
| **CPU** | 4 核心 |
| **内存** | 8 GB |
| **硬盘** | 10 GB 可用空间 |
| **Python** | 3.11.x（或安装包自带） |

### 推荐配置

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 11 64 位 |
| **CPU** | 8 核心 |
| **内存** | 16 GB |
| **硬盘** | 20 GB 可用空间（SSD） |
| **Python** | 3.11.9 |

### 必需软件

| 软件 | 版本 | 用途 |
|------|------|------|
| **Visual C++ 2015-2022** | 最新版 | PaddlePaddle/PyMuPDF/NumPy 依赖 |
| **LM Studio** | 最新版 | LLM 和 Embedding 服务 |

---

## 🔧 依赖版本

### 核心依赖（已锁定版本）

| 依赖 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.11.9 | 运行环境 |
| **ChromaDB** | 1.5.6 | 向量数据库 |
| **Flask** | 3.3 | Web 框架 |
| **PyMuPDF** | 1.27.2.2 | PDF 处理 |
| **python-docx** | 1.2.0 | Word 处理 |
| **openpyxl** | 3.3.5 | Excel 处理 |
| **python-pptx** | 1.0.2 | PPT 处理 |

### OCR 依赖（已锁定版本）

| 依赖 | 版本 | 用途 |
|------|------|------|
| **RapidOCR** | 3.8.1 | OCR 引擎（替代 PaddleOCR） |
| **ONNX Runtime** | 1.23.3 | 推理引擎 |
| **NumPy** | 2.4.4 | 数值计算（无版本限制） |
| **OpenCV** | 4.13.0 | 图像处理 |
| **Pillow** | 12.2.0 | 图片处理 |

### ✅ 版本优势

**RapidOCR 相比 PaddleOCR：**

```
✅ 无 protobuf 版本限制（copaw 可正常启动）
✅ 无 numpy ABI 版本限制
✅ 使用相同 PP-OCRv4 模型（识别质量不变）
✅ 离线安装包更小（节省 65MB）
✅ wheel 包自带 OCR 模型（无需联网下载）
```

### ⚠️ 已移除的依赖

```
❌ paddlepaddle（与 copaw protobuf 冲突）
❌ paddleocr（依赖 protobuf ≤3.30.2）
```

---

## 🛠️ 安装问题排查

### 问题 1：安装脚本无法运行

**症状：** 双击 install.bat 无反应或报错

**解决：**
```batch
# 右键点击 install.bat，选择"以管理员身份运行"
```

---

### 问题 2：Visual C++ 运行库安装失败

**症状：** 安装过程中提示 VC++ 安装失败

**解决：**
```batch
# 方法 1：手动下载安装
# 下载：https://aka.ms/vs/17/release/vc_redist.x64.exe
# 安装后重新运行 install.bat

# 方法 2：使用修复脚本
cd D:\RAG_Knowledge_Base
fix_vcredist.bat
```

---

### 问题 3：依赖安装失败

**症状：** pip install 报错

**解决：**
```bash
# 使用清华镜像源
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 如果仍有问题，逐个安装
python -m pip install chromadb==1.5.6 -i https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install flask==3.3 -i https://pypi.tuna.tsinghua.edu.cn/simple
# ...
```

---

### 问题 4：LM Studio 连接失败

**症状：** 查询时报错"Connection refused"

**解决：**
1. 确认 LM Studio 已启动
2. 确认本地服务器已开启（端口 1234）
3. 确认模型已加载
4. 检查防火墙设置

---

### 问题 5：OCR 功能无法使用

**症状：** 图片 PDF 无法识别

**解决：**
```bash
# 检查 RapidOCR 是否正常
python -c "from rapidocr import RapidOCR; print('OK')"

# 如果报错，重新安装
python -m pip install rapidocr onnxruntime -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 📖 使用文档

安装完成后，请阅读以下文档：

| 文档 | 用途 |
|------|------|
| `docs/01-知识库使用说明.md` | 基础使用指南 |
| `docs/10-系统架构说明.md` | 系统架构设计 |
| `docs/24-命令速查表.md` | 命令参考 |
| `docs/30-OCR 功能使用指南.md` | OCR 功能使用 |
| `docs/41-常见问题排查.md` | 问题排查 |

---

## 🎯 验证安装

### 快速验证脚本

```batch
# 创建验证脚本 verify_installation.bat
@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════════╗
echo ║       RAG 知识库系统 - 安装验证                    ║
echo ╚════════════════════════════════════════════════════╝
echo.

echo [1/5] 检查 Python 版本...
python --version
if errorlevel 1 (
    echo ❌ Python 未安装
    exit /b 1
)
echo ✅ Python 正常
echo.

echo [2/5] 检查核心依赖...
python -c "import chromadb; import flask; import pymupdf" 2>nul
if errorlevel 1 (
    echo ❌ 核心依赖缺失
    exit /b 1
)
echo ✅ 核心依赖正常
echo.

echo [3/5] 检查 OCR 依赖...
python -c "from rapidocr import RapidOCR" 2>nul
if errorlevel 1 (
    echo ⚠️  OCR 依赖未安装（可选功能）
) else (
    echo ✅ OCR 依赖正常
)
echo.

echo [4/5] 检查 LM Studio 连接...
curl http://127.0.0.1:1234/health 2>nul | findstr "ok" >nul
if errorlevel 1 (
    echo ⚠️  LM Studio 未连接（请先启动 LM Studio）
) else (
    echo ✅ LM Studio 连接正常
)
echo.

echo [5/5] 检查知识库初始化...
python -c "from core import KnowledgeBase; kb = KnowledgeBase(); print('OK')" 2>nul
if errorlevel 1 (
    echo ❌ 知识库初始化失败
    exit /b 1
)
echo ✅ 知识库初始化正常
echo.

echo ╔════════════════════════════════════════════════════╗
echo ║           ✅ 安装验证通过！                        ║
echo ╚════════════════════════════════════════════════════╝
pause
```

---

## 📊 安装包清单

### 核心文件

- [x] `core/core.py` - KnowledgeBase 核心类
- [x] `core/copaw_skill.py` - CoPaw 技能封装
- [x] `core/__init__.py` - 包初始化

### 工具脚本

- [x] `tools/rag_interactive.py` - 交互式管理工具
- [x] `tools/rag_qa.py` - 快速问答工具
- [x] `tools/ocr_processor.py` - OCR 处理核心
- [x] `tools/ocr_simple.py` - 简化版 OCR
- [x] `tools/ocr_pdf.py` - PDF OCR 工具

### 批处理工具

- [x] `tools/RAG 知识库管理工具.bat`
- [x] `tools/PDF OCR 处理工具.bat`
- [x] `tools/RAG 诊断工具.bat`
- [x] `tools/安装 OCR 依赖.bat`

### Web 界面

- [x] `web/web_app.py` - Flask Web 应用
- [x] `web/启动 Web 界面.bat` - Web 启动脚本
- [x] `web/templates/index.html` - Web 界面 HTML

### 使用文档

- [x] `docs/00-文档目录.md`
- [x] `docs/01-知识库使用说明.md`
- [x] `docs/10-系统架构说明.md`
- [x] `docs/24-命令速查表.md`
- [x] `docs/30-OCR 功能使用指南.md`
- [x] `docs/40-系统状态检查.md`
- [x] `docs/41-常见问题排查.md`
- [x] `docs/50-Skill 技能说明.md`

### 安装脚本

- [x] `install.bat` - 主安装脚本
- [x] `requirements.txt` - 依赖列表
- [x] `check_environment.bat` - 环境检测
- [x] `start_all.bat` - 启动服务
- [x] `stop_all.bat` - 停止服务
- [x] `status.bat` - 服务状态
- [x] `fix_vcredist.bat` - 修复 VC++

---

## 📞 技术支持

### 常见问题

查看 `docs/41-常见问题排查.md`

### 系统架构

查看 `docs/10-系统架构说明.md`

### 命令参考

查看 `docs/24-命令速查表.md`

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| **v3.3** | 2026-04-22 | ✅ RapidOCR 替代 PaddleOCR（解决 protobuf 冲突）<br>✅ wheel 包自带 OCR 模型（无需联网下载）<br>✅ 离线安装包优化（节省 65MB）<br>✅ numpy/protobuf 无版本限制 |
| **v3.0** | 2026-04-15 | ✅ 添加 API Key 认证支持<br>✅ 修复参数名不一致问题（force_rebuild → force）<br>✅ 更新核心代码同步现网版本 |
| **v2.9** | 2026-04-14 | ✅ 升级到 Python 3.11.9 嵌入式版本<br>✅ 下载 cp311 专用 whl 依赖包<br>✅ 更新安装脚本支持新版本<br>✅ 与实际运行环境完全一致 |
| **v2.1** | 2026-04-07 | ✅ 更新 Python 3.11.9<br>✅ 更新 ChromaDB 1.5.6<br>✅ 更新 Flask 3.3<br>✅ 更新 PaddleOCR 2.7.3<br>✅ 修复 Word 文档 OCR 功能<br>✅ 添加 Web 界面初始化功能 |
| v2.0 | 2026-04-03 | 初始分发版本 |

---

## ✅ 安装检查清单

安装完成后，请确认以下项目：

- [ ] Python 3.11.9 已安装
- [ ] Visual C++ 2015-2022 运行库已安装
- [ ] 所有依赖包已安装（运行 verify_installation.bat）
- [ ] LM Studio 已安装并配置
- [ ] LLM 模型已下载（qwen/qwen3.5-9b）
- [ ] Embedding 模型已下载（text-embedding-qwen3-embedding-4b）
- [ ] **API Key 已配置**（如果 LM Studio 开启认证，请填写 config/.env）
- [ ] Web 界面可以正常访问（http://localhost:5000）
- [ ] 知识库可以正常查询
- [ ] OCR 功能可以正常使用（上传含图片的 Word 文档测试）

---

## 🎉 总结

**RAG 知识库安装包 v2.1 特点：**

- ✅ **完整** - 包含所有必需组件
- ✅ **稳定** - 所有版本经过测试验证
- ✅ **易用** - 一键安装，双击运行
- ✅ **离线** - 支持无网络环境安装
- ✅ **文档齐全** - 15+ 个使用说明文档

**目标：** 让其他同事拿到后可以快速部署，不会出现版本不兼容、文件缺失等问题。

---

**🌸 祝安装顺利！**

**创建日期：** 2026-04-07  
**维护团队：** RAG 知识库团队
