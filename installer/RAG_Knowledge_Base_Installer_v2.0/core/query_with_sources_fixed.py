    def query_with_sources(self, question: str, top_k: int = 5) -> QueryResult:
        """带引用来源的查询"""
        self.add_documents()
        docs = self.vectorstore.similarity_search(question, k=top_k)
        
        if not docs:
            return QueryResult("未在知识库中找到相关信息。", [], question, datetime.now().isoformat())
        
        # 构建上下文 - 只保留相关的文档片段
        context_parts = []
        sources = []
        
        # 提取问题中的关键词
        question_keywords = ["职责", "负责", "任务", "工作", "管理", "总部", "大区", "团队", "虚拟"]
        
        for i, doc in enumerate(docs):
            content = doc.page_content
            
            # 只保留包含关键词的文档
            has_keyword = any(kw in content for kw in question_keywords)
            
            if has_keyword:
                preview = content[:600]
                context_parts.append(f"[来源{i+1}] {preview}")
                sources.append({
                    "index": i + 1,
                    "source": doc.metadata.get("source", "未知"),
                    "content_preview": preview[:150]
                })
        
        # 如果没有过滤出任何内容，使用原始检索结果（前 3 个）
        if not context_parts:
            for i, doc in enumerate(docs[:3]):
                preview = doc.page_content[:400]
                context_parts.append(f"[来源{i+1}] {preview}")
                sources.append({
                    "index": i + 1,
                    "source": doc.metadata.get("source", "未知"),
                    "content_preview": preview[:150]
                })
        
        context = "\n\n".join(context_parts)
        
        # 构建 prompt - 参考成功的 query_virtual_team.py
        prompt = f"""基于以下文档内容，回答问题。

文档内容：
{context}

问题：{question}

请根据文档内容回答。如果文档中没有明确提及相关信息，请总结文档中与之相关的内容。

答案："""

        # 调用 Ollama
        response = ollama.generate(
            model=self.llm_model,
            prompt=prompt,
            options={"temperature": 0, "think": False}
        )
        
        answer = response.get("response", "")
        
        # 如果答案为空或包含思考过程，尝试清理
        if not answer or len(answer) > 500:
            # 可能是思考过程，尝试提取
            if "答案：" in answer:
                answer = answer.split("答案：")[-1].strip()
            elif "根据" in answer and "文档" in answer:
                # 提取"根据文档"开始的内容
                idx = answer.find("根据")
                if idx >= 0:
                    answer = answer[idx:].split("\n\n")[0]
        
        # 如果还是空，返回检索到的内容
        if not answer:
            answer = "根据检索到的文档，相关内容如下：\n\n" + context[:600]
        
        return QueryResult(
            answer=answer,
            sources=sources,
            query=question,
            timestamp=datetime.now().isoformat()
        )
