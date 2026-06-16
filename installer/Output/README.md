# 📦 RAG-Local Knowledge Base v3.7 安装包

**版本：** v3.7
**发布日期：** 2026-05-06
**文件：** `RAG-Local_v3.7_Portable.zip` (260.6 MB)

---

## 🆕 v3.7 新增功能

### ⚙️ LLM 模型配置 Web UI
- Web 界面直接配置 LLM/Embedding 参数，无需手动编辑 .env
- 一键测试 LLM 服务连接，获取可用模型列表
- 配置保存到 .env 文件

### 🚀 PDF 混合 OCR 优化
- 多页采样检测，智能判断文本/图片比例
- 文本页用原生提取，图片页用 RapidOCR
- 混合 PDF 处理时间从数分钟降至秒级

### 📊 Excel 结构化数据分析
- 单文件查询、多文件对比、跨月聚合、跨城市对比
- 文件名智能解析（城市YYYYMM类别.xlsx）

---

## 📦 安装包内容

| 组件 | 版本 |
|------|------|
| Python 嵌入式 | 3.11.9 |
| ChromaDB | 1.5.6 |
| Flask | 3.1.3 |
| PyMuPDF | 1.27.2.2 |
| RapidOCR | 3.8.1 |
| pandas | 3.0.2 |
| 所有依赖 | 离线 wheel 包 |

---

## 🚀 安装步骤

1. 解压 `RAG-Local_v3.7_Portable.zip` 到目标目录
2. 运行 `install.bat`（以管理员身份）
3. 安装过程自动：安装 VC++ 运行库 → pip → Python 依赖 → 配置向导
4. 完成后运行 `start_all.bat` 启动服务
5. 浏览器访问 `http://localhost:5000`

---

## 📝 Inno Setup 编译说明

本目录同时提供了 `setup.iss` 脚本，使用 Inno Setup 6 可以编译 `.exe` 安装包：

```
iscc "F:\RAG_Knowledge_Base\installer\RAG_Knowledge_Base_Installer_v2.0\setup.iss"
```

输出：`F:\RAG_Knowledge_Base\installer\Output\RAG-Local_v3.7_Setup.exe`

---

**🌸 感谢使用 RAG-Local 知识库管理系统！**