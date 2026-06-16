"""
RAG Q&A for Knowledge Base
"""
import os
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pymupdf
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama

print("=" * 60)
print("RAG Q&A - Knowledge Base")
print("=" * 60)

# Config
DOC_PATH = r"D:\RAG_Knowledge_Base\documents\pdf\附件 1：中国移动云化核心网建设指导意见（2021 版）.pdf"
# Alternative path if Chinese chars cause issues
import glob
pdf_files = glob.glob(r"D:\RAG_Knowledge_Base\documents\pdf\*.pdf")
print(f"Found PDF files: {pdf_files}")
DOC_PATH = [f for f in pdf_files if "中国移动" in f or "云化" in f][0] if pdf_files else DOC_PATH
print(f"Using: {DOC_PATH}")
COLLECTION_NAME = "knowledge_base_docs"
OLLAMA_MODEL = "qwen3.5:4b"
EMBED_MODEL = "nomic-embed-text"
DB_PATH = r"./chroma_kb_db"

# Step 1: Read PDF
print("\n[Step 1/5] Reading PDF...")
doc = pymupdf.open(DOC_PATH)
full_text = ""
for page in doc:
    full_text += page.get_text()
doc.close()
print(f"  [OK] PDF read: {len(full_text)} chars")

# Step 2: Chunk
print("\n[Step 2/5] Chunking...")
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
chunks = splitter.split_text(full_text)
print(f"  [OK] Created {len(chunks)} chunks")

# Step 3: Embed & Store
print("\n[Step 3/5] Embedding & Storing...")
embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url="http://localhost:11434")
if os.path.exists(DB_PATH):
    import shutil
    shutil.rmtree(DB_PATH)
vectorstore = Chroma.from_texts(texts=chunks, embedding=embeddings, 
                                 persist_directory=DB_PATH, collection_name=COLLECTION_NAME)
print(f"  [OK] Stored in ChromaDB")

# Step 4: Retrieve
print("\n[Step 4/5] Retrieving...")
query = "根据项目组织要求和责任分工，总部职责是什么？"
docs = vectorstore.similarity_search(query, k=5)
print(f"  Query: {query}")
print(f"  Found {len(docs)} relevant chunks")

# Show retrieved chunks
print("\n--- Retrieved Chunks ---")
for i, doc in enumerate(docs):
    print(f"\n[{i+1}] {doc.page_content[:400]}...")

# Step 5: Generate
print("\n" + "=" * 60)
print("[Step 5/5] Generating answer...")
context = "\n".join([doc.page_content for doc in docs])

response = ollama.chat(
    model=OLLAMA_MODEL,
    messages=[
        {
            "role": "user",
            "content": f"""基于以下文档内容回答问题。

文档内容：
{context}

问题：{query}

请根据文档内容，清晰列出总部的职责。如果文档中没有相关信息，请说明。"""
        }
    ],
    options={"temperature": 0}
)
answer = response["message"]["content"]
print(f"\n{'='*60}")
print("ANSWER:")
print("=" * 60)
print(answer)
print("=" * 60)
