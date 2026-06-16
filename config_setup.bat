@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "INSTALL_DIR=%~1"
set "ENV_FILE=!INSTALL_DIR!\config\.env"

echo.
echo ============================================================
echo   RAG 知识库 - 配置修改工具 v3.2.1
echo ============================================================
echo.

REM 检查安装目录
if not defined INSTALL_DIR (
    echo [错误] 未指定安装目录！
    pause
    exit /b 1
)

REM 检查配置文件是否存在
if not exist "!ENV_FILE!" (
    echo [错误] 配置文件不存在: !ENV_FILE!
    pause
    exit /b 1
)

echo [OK] 配置文件: !ENV_FILE!
echo.

REM ============================================================
REM 显示当前配置
REM ============================================================
echo ============================================================
echo   当前配置
echo ============================================================
echo.

REM 使用 findstr 读取当前值
for /f "usebackq tokens=2 delims==" %%a in (`findstr "LLM_BASE_URL=" "!ENV_FILE!" 2^>nul`) do set "CURRENT_LLM_URL=%%a"
for /f "usebackq tokens=2 delims==" %%a in (`findstr "LLM_MODEL=" "!ENV_FILE!" 2^>nul`) do set "CURRENT_LLM_MODEL=%%a"
for /f "usebackq tokens=2 delims==" %%a in (`findstr "^API_KEY=" "!ENV_FILE!" 2^>nul`) do set "CURRENT_API_KEY=%%a"
for /f "usebackq tokens=2 delims==" %%a in (`findstr "EMBEDDING_BASE_URL=" "!ENV_FILE!" 2^>nul`) do set "CURRENT_EMBED_URL=%%a"
for /f "usebackq tokens=2 delims==" %%a in (`findstr "EMBEDDING_MODEL=" "!ENV_FILE!" 2^>nul`) do set "CURRENT_EMBED_MODEL=%%a"
for /f "usebackq tokens=2 delims==" %%a in (`findstr "EMBEDDING_API_KEY=" "!ENV_FILE!" 2^>nul`) do set "CURRENT_EMBED_KEY=%%a"

echo LLM 服务器: !CURRENT_LLM_URL!
echo LLM 模型: !CURRENT_LLM_MODEL!
echo LLM API Key: !CURRENT_API_KEY!
echo.
echo Embedding 服务器: !CURRENT_EMBED_URL!
echo Embedding 模型: !CURRENT_EMBED_MODEL!
echo Embedding API Key: !CURRENT_EMBED_KEY!
echo.
echo ============================================================
echo.

REM ============================================================
REM 第一部分：LLM 大模型配置
REM ============================================================
echo.
echo ============================================================
echo   第一部分：LLM 大模型配置
echo ============================================================
echo.
echo [说明] LLM 用于对话问答，需要配置服务器地址和模型
echo [提示] 直接按回车保持当前值不变
echo.

REM ============================================================
REM LLM Server URL
REM ============================================================
echo [步骤 1/3] 配置 LLM 服务器地址
echo 当前值: !CURRENT_LLM_URL!
echo 示例: http://127.0.0.1:1234 或 http://192.168.1.100:1234
echo.
set /p "LLM_BASE_URL=请输入新地址 (回车保持不变): "

if "!LLM_BASE_URL!"=="" (
    set "LLM_BASE_URL=!CURRENT_LLM_URL!"
    echo [OK] 保持原值: !LLM_BASE_URL!
) else (
    echo [OK] 新地址: !LLM_BASE_URL!
)
echo.

REM ============================================================
REM LLM Model Name
REM ============================================================
echo [步骤 2/3] 配置 LLM 模型名称
echo 当前值: !CURRENT_LLM_MODEL!
echo 常用模型: qwen/qwen3.5-9b, deepseek-r1, llama-3.1-8b
echo.
set /p "LLM_MODEL=请输入新模型 (回车保持不变): "

if "!LLM_MODEL!"=="" (
    set "LLM_MODEL=!CURRENT_LLM_MODEL!"
    echo [OK] 保持原值: !LLM_MODEL!
) else (
    echo [OK] 新模型: !LLM_MODEL!
)
echo.

REM ============================================================
REM LLM API Key
REM ============================================================
echo [步骤 3/3] 配置 LLM API Key
echo 当前值: !CURRENT_API_KEY!
echo [说明] 如果服务器不需要认证，请输入空值清除
echo.
set /p "LLM_API_KEY=请输入 API Key (回车保持不变): "

if "!LLM_API_KEY!"=="" (
    set "LLM_API_KEY=!CURRENT_API_KEY!"
    echo [OK] API Key 保持不变
) else (
    echo [OK] 新 API Key 已设置
)
echo.

echo ============================================================
echo   LLM 配置完成
echo ============================================================
echo   服务器: !LLM_BASE_URL!
echo   模型: !LLM_MODEL!
echo   API Key: !LLM_API_KEY!
echo ============================================================
echo.

REM ============================================================
REM 第二部分：Embedding 大模型配置
REM ============================================================
echo.
echo ============================================================
echo   第二部分：Embedding 大模型配置
echo ============================================================
echo.
echo [说明] Embedding 用于将文本转换为向量，支持语义搜索
echo [提示] 直接按回车保持当前值不变
echo        输入 "same" 可使用 LLM 服务器地址
echo.

REM ============================================================
REM Embedding Server URL
REM ============================================================
echo [步骤 1/3] 配置 Embedding 服务器地址
echo 当前值: !CURRENT_EMBED_URL!
echo.
set /p "EMBEDDING_BASE_URL=请输入新地址 (回车保持不变，输入 same 使用LLM地址): "

if "!EMBEDDING_BASE_URL!"=="" (
    set "EMBEDDING_BASE_URL=!CURRENT_EMBED_URL!"
    echo [OK] 保持原值: !EMBEDDING_BASE_URL!
) else if "!EMBEDDING_BASE_URL!"=="same" (
    set "EMBEDDING_BASE_URL=!LLM_BASE_URL!"
    echo [OK] 使用 LLM 地址: !EMBEDDING_BASE_URL!
) else (
    echo [OK] 新地址: !EMBEDDING_BASE_URL!
)
echo.

REM ============================================================
REM Embedding Model Name
REM ============================================================
echo [步骤 2/3] 配置 Embedding 模型名称
echo 当前值: !CURRENT_EMBED_MODEL!
echo 常用模型: text-embedding-qwen3-embedding-4b, text-embedding-3-small
echo.
set /p "EMBEDDING_MODEL=请输入新模型 (回车保持不变): "

if "!EMBEDDING_MODEL!"=="" (
    set "EMBEDDING_MODEL=!CURRENT_EMBED_MODEL!"
    echo [OK] 保持原值: !EMBEDDING_MODEL!"
) else (
    echo [OK] 新模型: !EMBEDDING_MODEL!"
)
echo.

REM ============================================================
REM Embedding API Key (独立配置)
REM ============================================================
echo [步骤 3/3] 配置 Embedding API Key (独立配置)
echo 当前值: !CURRENT_EMBED_KEY!
echo [说明] 如果 Embedding 使用不同的服务器，需要单独配置 API Key
echo        输入 "same" 可使用 LLM 的 API Key
echo        直接回车保持当前值不变
echo.
set /p "EMBEDDING_API_KEY=请输入 Embedding API Key (回车保持不变，输入 same 使用LLM的Key): "

if "!EMBEDDING_API_KEY!"=="" (
    set "EMBEDDING_API_KEY=!CURRENT_EMBED_KEY!"
    echo [OK] API Key 保持不变
) else if "!EMBEDDING_API_KEY!"=="same" (
    set "EMBEDDING_API_KEY=!LLM_API_KEY!"
    echo [OK] 使用 LLM API Key: !EMBEDDING_API_KEY!
) else (
    echo [OK] 新 API Key 已设置
)
echo.

echo ============================================================
echo   Embedding 配置完成
echo ============================================================
echo   服务器: !EMBEDDING_BASE_URL!
echo   模型: !EMBEDDING_MODEL!
echo   API Key: !EMBEDDING_API_KEY!
echo ============================================================
echo.

REM ============================================================
REM 保存配置 - 使用 PowerShell 替换特定参数
REM ============================================================
echo.
echo ============================================================
echo   保存配置
echo ============================================================
echo.
echo 正在更新配置文件...
echo.

REM 创建 PowerShell 替换脚本
set "PS_SCRIPT=!INSTALL_DIR!\config\replace_env.ps1"

(
echo $envFile = '!ENV_FILE!'
echo $content = Get-Content $envFile -Encoding UTF8
echo.
echo # 替换 LLM 参数
echo $content = $content -replace '^LLM_BASE_URL=.*', 'LLM_BASE_URL=!LLM_BASE_URL!'
echo $content = $content -replace '^LLM_MODEL=.*', 'LLM_MODEL=!LLM_MODEL!'
echo $content = $content -replace '^API_KEY=.*', 'API_KEY=!LLM_API_KEY!'
echo.
echo # 替换 Embedding 参数
echo $content = $content -replace '^EMBEDDING_BASE_URL=.*', 'EMBEDDING_BASE_URL=!EMBEDDING_BASE_URL!'
echo $content = $content -replace '^EMBEDDING_MODEL=.*', 'EMBEDDING_MODEL=!EMBEDDING_MODEL!'
echo $content = $content -replace '^EMBEDDING_API_KEY=.*', 'EMBEDDING_API_KEY=!EMBEDDING_API_KEY!'
echo.
echo # 保存文件
echo $content ^| Set-Content $envFile -Encoding UTF8
) > "!PS_SCRIPT!"

REM 执行 PowerShell 脚本
powershell -ExecutionPolicy Bypass -File "!PS_SCRIPT!"

REM 删除临时脚本
del "!PS_SCRIPT!"

echo [OK] 配置已保存到: !ENV_FILE!
echo.

REM ============================================================
REM 显示更新后的配置
REM ============================================================
echo.
echo ============================================================
echo   配置汇总
echo ============================================================
echo.
echo LLM 大模型配置:
echo   服务器地址: !LLM_BASE_URL!
echo   模型名称: !LLM_MODEL!
echo   API Key: !LLM_API_KEY!
echo.
echo Embedding 大模型配置:
echo   服务器地址: !EMBEDDING_BASE_URL!
echo   模型名称: !EMBEDDING_MODEL!
echo   API Key: !EMBEDDING_API_KEY!
echo.
echo ============================================================
echo   其他配置参数已保留不变
echo ============================================================
echo.

REM ============================================================
REM 配置完成提示
REM ============================================================
echo.
echo ============================================================
echo   配置修改完成！
echo ============================================================
echo.
echo [提示] 如需查看完整配置，请打开: !ENV_FILE!
echo.
echo [启动] 运行 start_all.bat 启动 Web 界面，访问 http://localhost:5000
echo.
pause