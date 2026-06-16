# RAG 知识库检索技能

## 功能说明
通过检索本地知识库（`D:\RAG_Knowledge_Base\documents`）回答用户问题。

## 触发条件
- 用户提到"查一下知识库"、"检索文档"、"根据文档"等
- 用户询问与已加载文档相关的问题
- 用户明确提到"总部职责"、"电费"、"项目组织"等文档内容

## 使用方法

### 在 CoPaw 对话中直接使用
```
用户：查一下知识库，总部职责是什么？
助手：[自动调用 RAG 检索并回答]
```

### Python API
```python
from rag_tool import KnowledgeBase

kb = KnowledgeBase()
answer = kb.query("总部职责是什么？")
```

### 带引用来源
```python
result = kb.query_with_sources("总部职责是什么？")
print(result.answer)
print(result.sources)  # 显示来源文档
```

## 支持的文档格式
- PDF (.pdf)
- Word (.docx)
- 文本 (.txt, .md)
- Excel (.xlsx, .xls, .csv)

## 自动加载机制
- 文档放入 `D:\RAG_Knowledge_Base\documents` 后自动检测
- 首次查询时自动加载新增/修改的文档
- 增量更新，无需重建整个索引

## 配置说明
- 文档路径：`D:\RAG_Knowledge_Base\documents`
- 数据库路径：`D:\RAG_Knowledge_Base\documents\.rag\chroma_db`
- Embedding 模型：`nomic-embed-text` (Ollama)
- LLM 模型：`qwen3.5:4b` (Ollama)
