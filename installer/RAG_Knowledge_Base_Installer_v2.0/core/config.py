"""
RAG 知识库 - 集中化配置模块
从 .env 加载 / 写入 LLM 配置，提供统一的读/写接口
"""
import os
import re
from dotenv import load_dotenv

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.dirname(CORE_DIR)
ENV_PATH = os.path.join(INSTALL_DIR, "config", ".env")

DEFAULTS = {
    "LLM_BASE_URL": "http://127.0.0.1:1234",
    "LLM_MODEL": "qwen/qwen3.5-9b",
    "API_KEY": "",
    "EMBEDDING_BASE_URL": "",
    "EMBEDDING_MODEL": "text-embedding-qwen3-embedding-4b",
    "EMBEDDING_API_KEY": ""
}


def load_settings() -> dict:
    """从 .env 文件加载全部配置（带默认值）"""
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH, override=True)

    settings = {}
    for key, default in DEFAULTS.items():
        settings[key] = os.getenv(key, default)

    if not settings["EMBEDDING_BASE_URL"]:
        settings["EMBEDDING_BASE_URL"] = settings["LLM_BASE_URL"]
    if not settings["EMBEDDING_API_KEY"]:
        settings["EMBEDDING_API_KEY"] = settings["API_KEY"]

    return settings


def save_settings(config: dict) -> None:
    """保存配置到 .env 文件（只更新传入的字段，其余不变）"""
    os.makedirs(os.path.dirname(ENV_PATH), exist_ok=True)

    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = ""

    for key, value in config.items():
        if value is not None and key in DEFAULTS:
            if re.search(rf"^{key}=", content, re.MULTILINE):
                content = re.sub(rf"^{key}=.*$", f"{key}={value}", content, flags=re.MULTILINE)
            else:
                content += f"\n{key}={value}"

    with open(ENV_PATH, 'w', encoding='utf-8') as f:
        f.write(content.lstrip('\n') + '\n')
