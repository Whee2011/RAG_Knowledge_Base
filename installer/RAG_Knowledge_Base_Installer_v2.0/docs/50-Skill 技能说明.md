# 🤖 RAG 知识库 - Skill 技能说明

**版本：** v3.0  
**更新日期：** 2026-04-15  
**适合人群：** OpenClaw 开发者、系统集成人员

---

## 📖 本章内容

介绍如何将 RAG 知识库作为技能集成到 OpenClaw 平台，支持通过自然语言调用知识库查询功能。

---

## 🎯 功能概述

### Skill 名称
`rag_knowledge`

### 功能描述
RAG 知识库查询技能，支持通过自然语言查询本地知识库文档，获取基于文档的智能答案。

### 核心能力

- ✅ **语义查询** - 理解自然语言问题
- ✅ **文档检索** - 从知识库检索相关文档
- ✅ **答案生成** - 基于检索结果生成答案
- ✅ **来源标注** - 标注答案来源文档
- ✅ **多轮对话** - 支持上下文关联查询

---

## 🔧 技能配置

### OpenClaw 配置示例

**配置文件：** `openclaw.json`

```json
{
  "skills": [
    {
      "name": "rag_knowledge",
      "type": "python",
      "path": "<INSTALL_DIR>\\skills\\rag_knowledge",
      "description": "RAG 知识库查询技能，支持查询本地文档库",
      "enabled": true,
      "triggers": [
        "查询知识库",
        "搜索文档",
        "查找资料",
        "检索资料",
        "知识库中查找",
        "文档中搜索"
      ],
      "config": {
        "documents_path": "<INSTALL_DIR>\\documents",
        "chroma_db_path": "<INSTALL_DIR>\\documents\\.rag\\chroma_db",
        "llm_base_url": "http://127.0.0.1:1234",
        "llm_model": "qwen/qwen3.5-9b",
        "embedding_model": "text-embedding-qwen3-embedding-4b",
        "top_k": 2,
        "auto_refresh": false
      }
    }
  ]
}
```

---

## 📋 触发条件

### 自然语言触发

当用户输入包含以下关键词时，自动调用 RAG 知识库技能：

| 触发词 | 示例 |
|--------|------|
| 查询知识库 | "查询知识库中关于电费的信息" |
| 搜索文档 | "搜索文档中有关人工智能的内容" |
| 查找资料 | "查找资料，帮我看看合同条款" |
| 检索资料 | "检索一下项目报告" |
| 知识库中查找 | "知识库中查找 2026 年的报告" |
| 文档中搜索 | "文档中搜索关于预算的信息" |

### 配置触发词

在 OpenClaw 配置中添加自定义触发词：

```json
"triggers": [
  "查询知识库",
  "搜索文档",
  "查找资料",
  "你的自定义触发词"
]
```

---

## 💬 使用示例

### 示例 1：查询电费信息

**用户输入：**
```
查询知识库中关于电费的信息
```

**AI 响应：**
```
[调用 RAG 知识库技能]

根据知识库文档，电费相关信息如下：

📊 电费信息：
- 电费金额：[数值] 元
- 用电量：[数值] 千瓦时
- 电费周期：2026 年 2 月

📄 来源文档：
1. [账单名称].pdf - 第 1 页
2. [研究报告].docx - 第 3 页

需要我详细解释某项数据吗？
```

---

### 示例 2：搜索项目报告

**用户输入：**
```
搜索一下项目报告的内容
```

**AI 响应：**
```
[调用 RAG 知识库技能]

根据知识库中的项目报告：

📋 项目概况：
- 项目名称：[项目名称]
- 项目周期：[时间范围]
- 项目状态：[进行中/已完成]

📄 来源文档：
1. [项目报告].pdf - 第 1-5 页

需要了解更多细节吗？
```

---

### 示例 3：查找合同条款

**用户输入：**
```
帮我查找合同中的付款条款
```

**AI 响应：**
```
[调用 RAG 知识库技能]

根据知识库中的合同文档，付款条款如下：

💰 付款条款：
1. 首付款：合同签订后 5 个工作日内支付 [比例]%
2. 进度款：项目完成 [比例]% 后支付
3. 尾款：项目验收合格后支付剩余款项

📄 来源文档：
1. [合同名称].pdf - 第 3 页

需要查看完整合同吗？
```

---

## 🔌 API 接口

### 技能调用接口

**Python 调用：**
```python
from active_skills.rag_knowledge.rag_skill import rag_query

# 基本查询
result = rag_query("问题内容")

# 带参数查询
result = rag_query(
    "问题内容",
    top_k=2,
    auto_refresh=False
)

# 获取结果
print(result["answer"])
print(result["sources"])
```

**返回格式：**
```json
{
  "answer": "答案内容",
  "sources": [
    {
      "file": "文档.pdf",
      "content": "相关文本内容",
      "page": 1
    }
  ],
  "stats": {
    "prompt_tokens": 1000,
    "completion_tokens": 200,
    "query_time": 3.5
  }
}
```

---

### Web API 调用

**HTTP 请求：**
```http
POST http://localhost:5000/api/query
Content-Type: application/json

{
  "query": "问题内容",
  "top_k": 2,
  "auto_refresh": false
}
```

**响应：**
```json
{
  "answer": "答案内容",
  "sources": [...],
  "stats": {...}
}
```

---

## ⚙️ 参数配置

### 技能参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `top_k` | int | 2 | 检索文档数量 |
| `auto_refresh` | bool | false | 自动刷新索引 |
| `similarity_threshold` | float | 0.3 | 相似度阈值 |
| `max_tokens` | int | 2048 | 最大生成 Token 数 |

### 配置示例

```json
"config": {
  "top_k": 2,
  "auto_refresh": false,
  "similarity_threshold": 0.3,
  "max_tokens": 2048
}
```

---

## 🎯 最佳实践

### 1. 触发词优化

**推荐：**
```json
"triggers": [
  "查询知识库",
  "搜索文档",
  "查找资料",
  "检索",
  "查找",
  "搜索"
]
```

**避免：**
- 过于宽泛的词（如"查"）
- 与其他技能冲突的词

### 2. 答案格式

**推荐格式：**
```
[技能调用标识]

答案内容...

📄 来源文档：
1. 文档 1 - 第 X 页
2. 文档 2 - 第 Y 页

[后续问题引导]
```

### 3. 错误处理

```python
try:
    result = rag_query("问题")
    if not result["answer"]:
        return "抱歉，知识库中没有找到相关信息"
    return result["answer"]
except Exception as e:
    return f"查询失败：{str(e)}"
```

---

## 🔍 故障排查

### 问题 1：技能未触发

**症状：**
- 输入触发词后无响应
- AI 未调用知识库技能

**检查：**
1. 技能是否启用 (`"enabled": true`)
2. 触发词是否配置正确
3. 技能路径是否正确

**解决：**
```json
{
  "enabled": true,
  "path": "<INSTALL_DIR>\\skills\\rag_knowledge"
}
```

---

### 问题 2：查询失败

**症状：**
```
❌ 查询失败：Collection 不存在
```

**原因：**
- 索引未创建
- 路径配置错误

**解决：**
```batch
# 刷新索引
python D:\RAG_Knowledge_Base\core\core.py refresh

# 检查路径
python D:\RAG_Knowledge_Base\core\core.py status
```

---

### 问题 3：答案不准确

**症状：**
- 答案与问题不相关
- 检索结果质量差

**原因：**
- top_k 太小
- 相似度阈值太高

**解决：**
```json
{
  "top_k": 3,
  "similarity_threshold": 0.2
}
```

---

## 📊 性能优化

### 1. 减少响应时间

```json
{
  "top_k": 2,
  "auto_refresh": false
}
```

### 2. 提高答案质量

```json
{
  "top_k": 3,
  "max_tokens": 2048
}
```

### 3. 上下文管理

```python
# 保存查询历史
query_history = []

def rag_query_with_context(question, history=query_history):
    # 添加上下文
    context = "\n".join(history[-3:])
    full_question = f"{context}\n{question}"
    
    result = rag_query(full_question)
    
    # 更新历史
    history.append(question)
    
    return result
```

---

## 📚 集成示例

### 完整集成代码

```python
# openclaw_skills/rag_knowledge_skill.py

from active_skills.rag_knowledge.rag_skill import rag_query

class RAGKnowledgeSkill:
    """RAG 知识库技能"""
    
    def __init__(self, config):
        self.config = config
        self.name = "rag_knowledge"
        self.description = "RAG 知识库查询技能"
    
    def execute(self, query, context=None):
        """执行查询"""
        try:
            # 调用 RAG 查询
            result = rag_query(
                query,
                top_k=self.config.get("top_k", 2),
                auto_refresh=self.config.get("auto_refresh", False)
            )
            
            # 格式化响应
            response = self.format_response(result)
            
            return {
                "success": True,
                "response": response,
                "sources": result.get("sources", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def format_response(self, result):
        """格式化响应"""
        answer = result.get("answer", "")
        sources = result.get("sources", [])
        
        # 添加来源标注
        if sources:
            answer += "\n\n📄 来源文档：\n"
            for i, src in enumerate(sources, 1):
                answer += f"{i}. {src['file']} - 第{src.get('page', '?')}页\n"
        
        return answer

# 注册技能
skill = RAGKnowledgeSkill(config={
    "top_k": 2,
    "auto_refresh": False
})
```

---

## 📋 配置检查清单

在部署技能前，请检查：

- [ ] 技能路径配置正确
- [ ] 触发词配置合理
- [ ] 知识库索引已创建
- [ ] LM Studio 服务运行中
- [ ] 测试查询功能正常
- [ ] 错误处理完善
- [ ] 日志记录启用

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| [01-知识库使用说明.md](01-知识库使用说明.md) | 使用方式总览 |
| [24-命令速查表.md](24-命令速查表.md) | 常用命令 |

---

## 📞 技术支持

如遇到问题，请：

1. 查看技能日志
2. 检查配置文件
3. 测试独立查询功能
4. 联系技术支持

---

**文档维护：** RAG 知识库团队  
**更新日期：** 2026-04-15
