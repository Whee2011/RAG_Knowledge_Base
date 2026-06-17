# -*- coding: utf-8 -*-
"""
RAG 知识库 Web 界面
基于 Flask 的 Web 操作界面
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import json
from datetime import datetime
import hashlib
from dotenv import load_dotenv

# ==================== 动态路径配置 ====================
# 获取 web_app.py 所在目录（web 目录）
WEB_DIR = os.path.dirname(os.path.abspath(__file__))
# 安装目录 = web 目录的父目录
INSTALL_DIR = os.path.dirname(WEB_DIR)

# 添加核心代码路径（动态）
sys.path.insert(0, os.path.join(INSTALL_DIR, "core"))

from core import KnowledgeBase

app = Flask(__name__)

# 限制上传文件大小为 500MB
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

# 加载 .env 配置（动态路径）
load_dotenv(os.path.join(INSTALL_DIR, "config", ".env"))

# 从 .env 读取所有 LM Studio 配置
API_KEY = os.getenv("API_KEY", None)
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://127.0.0.1:1234")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3.5-9b")
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", LLM_BASE_URL)  # 默认使用 LLM 地址
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-qwen3-embedding-4b")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", API_KEY)  # 默认使用 LLM 的 API Key

# 配置（动态路径）
DOCUMENTS_PATH = os.path.join(INSTALL_DIR, "documents")
UPLOAD_FOLDER = os.path.join(DOCUMENTS_PATH, "uploads")
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'xlsx', 'xls', 'csv', 'txt', 'md', 'pptx', 'ppt'}

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 全局知识库实例（单例模式）
kb_instance = None


def secure_document_path(filepath: str) -> str:
    """验证并返回安全的文档路径，防止路径遍历攻击"""
    full_path = os.path.normpath(os.path.join(DOCUMENTS_PATH, filepath))
    normalized_doc_path = os.path.normpath(DOCUMENTS_PATH)
    if not full_path.startswith(normalized_doc_path):
        raise ValueError('非法路径')
    return full_path


def get_kb():
    """获取知识库实例"""
    global kb_instance
    if kb_instance is None:
        kb_instance = KnowledgeBase(
            name="default",  # 使用 default 名称，与命令行工具一致
            documents_path=DOCUMENTS_PATH,
            api_key=API_KEY,
            embedding_api_key=EMBEDDING_API_KEY,
            lmstudio_base_url=LLM_BASE_URL,
            embedding_base_url=EMBEDDING_BASE_URL,
            embed_model=EMBEDDING_MODEL,
            llm_model=LLM_MODEL
        )
    return kb_instance

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_hash(filepath):
    """计算文件 MD5"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """获取知识库状态"""
    try:
        kb = get_kb()
        status = kb.get_status()
        
        return jsonify({
            'success': True,
            'data': {
                'total_documents': status.total_documents,
                'total_chunks': status.total_chunks,
                'last_updated': status.last_updated,
                'documents': status.documents
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/query', methods=['POST'])
def api_query():
    """查询知识库（智能检索 - 自动判断向量/混合）"""
    try:
        data = request.json
        question = data.get('question', '')
        top_k = data.get('top_k', 5)
        max_context_length = data.get('max_context_length', 8000)

        if not question:
            return jsonify({
                'success': False,
                'error': '问题不能为空'
            }), 400

        kb = get_kb()
        # 使用智能 query 方法，自动判断检索策略
        result = kb.query(question, top_k=top_k, max_context_length=max_context_length)
        
        return jsonify({
            'success': True,
            'data': {
                'answer': result.answer,
                'sources': result.sources,
                'query': result.query,
                'timestamp': result.timestamp,
                # Token 统计和耗时
                'prompt_tokens': result.prompt_tokens,
                'completion_tokens': result.completion_tokens,
                'total_tokens': result.total_tokens,
                'query_time': round(result.query_time, 2)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/refresh', methods=['POST'])
def api_refresh():
    """刷新索引"""
    try:
        data = request.json or {}
        force = data.get('force', False)
        auto_ocr = data.get('auto_ocr', True)
        
        kb = get_kb()
        kb.add_documents(force=force, auto_ocr=auto_ocr)
        
        status = kb.get_status()
        
        return jsonify({
            'success': True,
            'message': '索引刷新成功',
            'data': {
                'total_documents': status.total_documents,
                'total_chunks': status.total_chunks,
                'last_updated': status.last_updated
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/extract', methods=['POST'])
def api_extract():
    """从 Excel/CSV 文件中提取结构化数据"""
    try:
        data = request.json or {}
        question = data.get('question', '')
        fields = data.get('fields', [])
        top_k = data.get('top_k', 5)

        if not question:
            return jsonify({
                'success': False,
                'error': '问题不能为空'
            }), 400

        kb = get_kb()
        result = kb.extract_data(question, fields=fields, top_k=top_k)

        return jsonify({
            'success': True,
            'data': {
                'answer': result.get('answer', ''),
                'operation': result.get('operation', ''),
                'sheet_name': result.get('sheet_name', ''),
                'row_count': result.get('row_count', 0),
                'value': result.get('value'),
                'data': result.get('data', []),
                'extracted_fields': result.get('extracted_fields', []),
                'error': result.get('error')
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/init', methods=['POST'])
def api_init():
    """初始化知识库索引（强制重建）"""
    try:
        data = request.json or {}
        auto_ocr = data.get('auto_ocr', True)
        
        kb = get_kb()
        
        # 删除现有 collection
        kb.delete_collection()
        
        # 重新创建并索引
        kb.add_documents(force=True, auto_ocr=auto_ocr)
        
        status = kb.get_status()
        
        return jsonify({
            'success': True,
            'message': '知识库初始化成功',
            'data': {
                'total_documents': status.total_documents,
                'total_chunks': status.total_chunks,
                'last_updated': status.last_updated
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """上传文件"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有文件'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '文件名为空'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'不支持的文件类型，支持的类型：{", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # 保存文件
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # 如果文件已存在，添加时间戳
        if os.path.exists(filepath):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        file.save(filepath)
        
        # 自动刷新索引
        kb = get_kb()
        kb.add_documents(auto_ocr=True)
        
        return jsonify({
            'success': True,
            'message': f'文件上传成功：{filename}',
            'data': {
                'filename': filename,
                'filepath': filepath,
                'size': os.path.getsize(filepath)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/files', methods=['GET'])
def api_files():
    """获取文件列表"""
    try:
        files = []
        for root, dirs, filenames in os.walk(DOCUMENTS_PATH):
            # 跳过隐藏目录和数据库目录
            if '.rag' in root or '__pycache__' in root:
                continue
            
            for filename in filenames:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, DOCUMENTS_PATH)
                # 转换为正斜杠（Web 标准），避免 JavaScript 反斜杠转义问题
                rel_path = rel_path.replace('\\', '/')
                
                # 跳过 OCR 生成的临时文件
                if filename.endswith('_ocr.txt'):
                    continue
                
                files.append({
                    'name': filename,
                    'path': rel_path,
                    'size': os.path.getsize(filepath),
                    'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S'),
                    'type': filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'unknown'
                })
        
        # 按修改时间排序
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/delete', methods=['POST'])
def api_delete():
    """删除文件"""
    try:
        data = request.json
        filepath = data.get('path', '')
        
        if not filepath:
            return jsonify({
                'success': False,
                'error': '文件路径不能为空'
            }), 400
        
        try:
            full_path = secure_document_path(filepath)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': '非法路径'
            }), 400

        if not os.path.exists(full_path):
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404

        # 删除文件
        os.remove(full_path)

        # 删除对应的 OCR 文件（如果有）
        base, _ = os.path.splitext(full_path)
        ocr_path = base + '_ocr.txt'
        if os.path.exists(ocr_path):
            os.remove(ocr_path)

        # 刷新索引
        kb = get_kb()
        kb.add_documents(force=True)

        return jsonify({
            'success': True,
            'message': f'文件已删除：{filepath}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ocr/<path:filepath>')
def api_ocr_file(filepath):
    """对指定文件进行 OCR"""
    try:
        try:
            full_path = secure_document_path(filepath)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': '非法路径'
            }), 400

        if not os.path.exists(full_path):
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        kb = get_kb()
        
        # 检测是否需要 OCR
        if kb._detect_need_ocr(full_path):
            # 执行 OCR（_auto_ocr 会自动生成 _ocr.txt 文件）
            kb._auto_ocr(full_path)

            # 推断 OCR 输出文件路径
            base, ext = os.path.splitext(full_path)
            ocr_txt_path = base + '_ocr.txt'

            return jsonify({
                'success': True,
                'message': 'OCR 完成',
                'data': {
                    'ocr_file': ocr_txt_path
                }
            })
        else:
            return jsonify({
                'success': True,
                'message': '文件不需要 OCR（已是文字 PDF 或其他格式）'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 RAG 知识库 Web 界面启动")
    print("=" * 60)
    print(f"📂 安装目录：{INSTALL_DIR}")
    print(f"📂 文档路径：{DOCUMENTS_PATH}")
    print(f"📁 上传目录：{UPLOAD_FOLDER}")
    print(f"🌐 访问地址：http://localhost:5000")
    print("=" * 60)
    print()
    
    # 从环境变量或配置读取 debug 模式，默认关闭
    debug_mode = os.getenv('WEB_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)