"""
混合检索模块 - Hybrid Search
结合向量检索 + BM25 关键词检索，提升召回率
"""

import numpy as np
from typing import List, Dict, Tuple, Any

try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25_AVAILABLE = False
    print("[WARNING] rank-bm25 未安装，混合检索将降级为纯向量检索")
    print("[INFO] 安装命令：pip install rank-bm25")


class HybridSearch:
    """
    混合检索类 - 向量检索 + BM25 关键词检索
    """
    
    def __init__(self, collection, embeddings, alpha: float = 0.5):
        """
        Args:
            collection: ChromaDB collection
            embeddings: Embedding 模型
            alpha: 向量检索权重 (0.5=向量 50% + 关键词 50%)
        """
        self.collection = collection
        self.embeddings = embeddings
        self.alpha = alpha
        self.bm25 = None
        self.all_chunks = []
        self.all_ids = []
        self.all_metadatas = []
        self.bm25_built = False
    
    def build_bm25_index(self):
        """构建 BM25 索引"""
        if not BM25_AVAILABLE:
            print("[WARNING] BM25 不可用，跳过索引构建")
            return
        
        print("[INFO] 构建 BM25 索引...")
        
        # 获取所有文档
        all_items = self.collection.get(include=['documents', 'metadatas'])
        self.all_chunks = all_items.get('documents', [])
        self.all_ids = all_items.get('ids', [])
        self.all_metadatas = all_items.get('metadatas', [])
        
        if not self.all_chunks:
            print("[WARNING] 无文档可构建 BM25 索引")
            return
        
        # 分词（中文按字符分词，英文按空格）
        tokenized_docs = []
        for chunk in self.all_chunks:
            # 简单分词：中文按字符，英文按单词
            tokens = list(chunk) if any('\u4e00' <= c <= '\u9fff' for c in chunk) else chunk.split()
            tokenized_docs.append(tokens)
        
        # 构建 BM25 索引
        self.bm25 = BM25Okapi(tokenized_docs)
        self.bm25_built = True
        print(f"[OK] BM25 索引构建完成 ({len(self.all_chunks)} 个文档块)")
    
    def _tokenize(self, text: str) -> List[str]:
        """分词"""
        return list(text) if any('\u4e00' <= c <= '\u9fff' for c in text) else text.split()
    
    def _normalize_scores(self, scores: List[float], reverse: bool = False) -> List[float]:
        """
        分数归一化到 0-1
        reverse: True 表示分数越小越好（如距离）
        """
        if not scores:
            return []
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            return [0.5] * len(scores)
        
        normalized = []
        for score in scores:
            if reverse:
                # 距离越小分数越高
                norm = 1 - (score - min_score) / (max_score - min_score)
            else:
                # 分数越大越好
                norm = (score - min_score) / (max_score - min_score)
            normalized.append(norm)
        
        return normalized
    
    def search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        混合检索主流程
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
        
        Returns:
            {
                'ids': [...],
                'documents': [...],
                'metadatas': [...],
                'scores': [...]
            }
        """
        # 如果 BM25 不可用，降级为纯向量检索
        if not BM25_AVAILABLE or not self.bm25_built:
            print("[INFO] 降级为纯向量检索")
            return self._vector_search(query, top_k)
        
        # 1. 向量检索（扩大范围）
        vector_top_k = min(top_k * 3, 20)
        vector_results = self._vector_search(query, vector_top_k)

        # 将向量距离（越小越好）归一化为正向分数（越大越好）
        if vector_results.get('scores'):
            vector_results['scores'] = self._normalize_scores(vector_results['scores'], reverse=True)

        # 2. BM25 关键词检索
        bm25_results = self._bm25_search(query, top_k * 3)

        # 将 BM25 分数（越大越好）归一化为 0-1 区间
        if bm25_results.get('scores'):
            bm25_results['scores'] = self._normalize_scores(bm25_results['scores'], reverse=False)

        # 3. 分数融合 (RRF - Reciprocal Rank Fusion)
        fused_results = self._fuse_results(vector_results, bm25_results, top_k)

        return fused_results
    
    def _vector_search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """纯向量检索"""
        query_embedding = self.embeddings.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        return {
            'ids': results['ids'][0] if results['ids'] else [],
            'documents': results['documents'][0] if results['documents'] else [],
            'metadatas': results['metadatas'][0] if results['metadatas'] else [],
            'scores': results['distances'][0] if 'distances' in results else [1.0] * len(results['ids'][0]) if results['ids'] else [],
            'type': 'vector'
        }
    
    def _bm25_search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """BM25 关键词检索"""
        if not self.bm25 or not self.all_chunks:
            return {'ids': [], 'documents': [], 'metadatas': [], 'scores': [], 'type': 'bm25'}
        
        # 计算 BM25 分数
        query_tokens = self._tokenize(query)
        bm25_scores = self.bm25.get_scores(query_tokens)
        
        # 获取 top_k，确保索引在有效范围内
        valid_indices = [i for i in range(len(bm25_scores)) if i < len(self.all_ids) and i < len(self.all_chunks)]
        top_indices = np.argsort([bm25_scores[i] for i in valid_indices])[::-1][:top_k]
        top_indices = [valid_indices[i] for i in top_indices if i < len(valid_indices)]
        
        return {
            'ids': [self.all_ids[i] for i in top_indices],
            'documents': [self.all_chunks[i] for i in top_indices],
            'metadatas': [self.all_metadatas[i] if i < len(self.all_metadatas) else {} for i in top_indices],
            'scores': [bm25_scores[i] for i in top_indices],
            'type': 'bm25'
        }
    
    def _fuse_results(self, vector_results: Dict, bm25_results: Dict, top_k: int) -> Dict[str, Any]:
        """
        融合向量检索和 BM25 结果
        使用 RRF (Reciprocal Rank Fusion) 倒数排名融合
        """
        # 构建 ID 到结果的映射
        vector_id_to_idx = {id: i for i, id in enumerate(vector_results['ids'])}
        bm25_id_to_idx = {id: i for i, id in enumerate(bm25_results['ids'])}
        
        # 收集所有 ID
        all_ids = set(vector_results['ids']) | set(bm25_results['ids'])
        
        # 计算 RRF 分数
        k = 60  # RRF 常数
        rrf_scores = {}
        
        for doc_id in all_ids:
            score = 0.0
            
            # 向量检索排名分数
            if doc_id in vector_id_to_idx:
                vector_rank = vector_id_to_idx[doc_id] + 1
                score += self.alpha * (1 / (k + vector_rank))
            
            # BM25 排名分数
            if doc_id in bm25_id_to_idx:
                bm25_rank = bm25_id_to_idx[doc_id] + 1
                score += (1 - self.alpha) * (1 / (k + bm25_rank))
            
            rrf_scores[doc_id] = score
        
        # 排序返回 top_k
        sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:top_k]
        
        # 构建返回结果
        all_results = {}
        for i, id in enumerate(vector_results['ids']):
            all_results[id] = {
                'document': vector_results['documents'][i],
                'metadata': vector_results['metadatas'][i],
                'score': rrf_scores.get(id, 0)
            }
        for i, id in enumerate(bm25_results['ids']):
            if id not in all_results:
                all_results[id] = {
                    'document': bm25_results['documents'][i],
                    'metadata': bm25_results['metadatas'][i],
                    'score': rrf_scores.get(id, 0)
                }
        
        return {
            'ids': sorted_ids,
            'documents': [all_results[id]['document'] for id in sorted_ids],
            'metadatas': [all_results[id]['metadata'] for id in sorted_ids],
            'scores': [all_results[id]['score'] for id in sorted_ids],
            'type': 'hybrid'
        }
