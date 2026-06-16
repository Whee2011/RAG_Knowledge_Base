; ============================================
; RAG-Local Knowledge Base Installer v3.7
; Full Installation - One Click Setup
; Date: 2026-05-06
; Changes from v3.6:
;   - Added: LLM model configuration UI (Settings panel)
;   - Added: GET/PUT /api/config/llm endpoints
;   - Added: POST /api/config/llm/test - test connection + list models
;   - Added: core/config.py centralized settings module
;   - Added: .env config save via Web UI
; Changes from v3.5.1:
;   - Added: Excel structured data analysis
;   - Added: pandas dependency
;   - Added: Hybrid PDF OCR (per-page detection + selective OCR)
;   - Fixed: OCR only image pages, skip text pages
;   - Fixed: Upload timeout (async indexing, 500MB limit)
; Changes from v3.5:
;   - Fixed: rank-bm25 included in requirements.txt
; Changes from v3.4:
;   - Fixed: rag_interactive.py documents list display
;   - Fixed: RAG 知识库管理工具.bat Python path
; ============================================

#define MyAppName "RAG-Local Knowledge Base"
#define MyAppVersion "3.7"
#define MyAppPublisher "RAG-Local Team"

[Setup]
AppId=RAGLocalKnowledgeBase_v37
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={sd}\RAG_Knowledge_Base
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=F:\RAG_Knowledge_Base\installer\Output
OutputBaseFilename=RAG-Local_v3.7_Setup
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern
SetupIconFile=RAG-Local.ico
UninstallDisplayIcon={app}\RAG-Local.ico
UninstallDisplayName={#MyAppName} v{#MyAppVersion}
VersionInfoVersion=3.7.0.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=RAG-Local Knowledge Base Full Installer v3.7 - LLM Config UI + Hybrid OCR
VersionInfoCopyright=2026
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion=3.7.0.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; Flags: unchecked

[Files]
; Root files
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.yaml.template"; DestDir: "{app}"; Flags: ignoreversion
Source: "start_all.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "stop_all.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "install.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "status.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "check_environment.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "check_integrity.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "download_packages.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "fix_vcredist.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "config_setup.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "RAG-Local.ico"; DestDir: "{app}"; Flags: ignoreversion

; Config files
Source: "config\.env"; DestDir: "{app}\config"; Flags: ignoreversion
Source: "config\.env.template"; DestDir: "{app}\config"; Flags: ignoreversion

; Core Python modules
Source: "core\*.py"; DestDir: "{app}\core"; Flags: ignoreversion
Source: "core\SKILL.md"; DestDir: "{app}\core"; Flags: ignoreversion

; Python embedded (解压后的文件，不是zip)
Source: "packages\python_embedded\*"; DestDir: "{app}\python_embedded"; Flags: ignoreversion recursesubdirs createallsubdirs

; get-pip
Source: "packages\get-pip.py"; DestDir: "{app}\packages"; Flags: ignoreversion

; Wheel packages (all dependencies)
Source: "packages\requirements_cp311\*.whl"; DestDir: "{app}\packages\requirements_cp311"; Flags: ignoreversion

; Requirements files
Source: "packages\requirements.txt"; DestDir: "{app}\packages"; Flags: ignoreversion
Source: "packages\requirements_rag.txt"; DestDir: "{app}\packages"; Flags: ignoreversion
Source: "packages\requirements_full.txt"; DestDir: "{app}\packages"; Flags: ignoreversion

; VC++ redistributable
Source: "packages\vcredist_x64.exe"; DestDir: "{app}\packages"; Flags: ignoreversion

; Web interface
Source: "web\*.py"; DestDir: "{app}\web"; Flags: ignoreversion
Source: "web\*.bat"; DestDir: "{app}\web"; Flags: ignoreversion
Source: "web\templates\*.html"; DestDir: "{app}\web\templates"; Flags: ignoreversion
Source: "web\static\*.png"; DestDir: "{app}\web\static"; Flags: ignoreversion

; Tools
Source: "tools\*.py"; DestDir: "{app}\tools"; Flags: ignoreversion
Source: "tools\*.bat"; DestDir: "{app}\tools"; Flags: ignoreversion

; Documentation
Source: "docs\*.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "*.md"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
; Create empty directories for user data
Name: "{app}\documents"; Flags: uninsneveruninstall
Name: "{app}\documents\.rag"; Flags: uninsneveruninstall
Name: "{app}\logs"; Flags: uninsneveruninstall
Name: "{app}\python_embedded\Lib"; Flags: uninsneveruninstall
Name: "{app}\python_embedded\Lib\site-packages"; Flags: uninsneveruninstall

[Icons]
; Start menu shortcuts
Name: "{group}\Start Web Interface"; Filename: "{app}\web\启动 Web 界面.bat"; WorkingDir: "{app}"
Name: "{group}\Start All Services"; Filename: "{app}\start_all.bat"; WorkingDir: "{app}"
Name: "{group}\Stop All Services"; Filename: "{app}\stop_all.bat"; WorkingDir: "{app}"
Name: "{group}\Check Status"; Filename: "{app}\status.bat"; WorkingDir: "{app}"
Name: "{group}\Check Environment"; Filename: "{app}\check_environment.bat"; WorkingDir: "{app}"
; Note: Chinese filename shortcuts removed due to encoding issues
; Users can access tools from the installation directory
Name: "{group}\Documentation"; Filename: "{app}\README.md"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"

; Desktop shortcut
Name: "{autodesktop}\RAG-Local Knowledge Base"; Filename: "{app}\start_all.bat"; WorkingDir: "{app}"; Tasks: desktopicon; IconFilename: "{app}\RAG-Local.ico"

[Run]
; 安装完成后自动执行的操作
; 1. 安装 VC++ redistributable
Filename: "{app}\packages\vcredist_x64.exe"; Description: "Installing VC++ runtime..."; StatusMsg: "Installing Visual C++ runtime..."; Flags: waituntilterminated runhidden

; 2. 安装 pip 23.3.1（支持 omegaconf 2.0.6）
Filename: "{app}\python_embedded\python.exe"; Parameters: "{app}\packages\get-pip.py pip==23.3.1 setuptools wheel"; StatusMsg: "Installing pip 23.3.1..."; Flags: waituntilterminated runhidden

; 3. 安装所有依赖包（使用 -r 读取 requirements.txt）
Filename: "{app}\python_embedded\python.exe"; Parameters: "-m pip install --no-index --find-links={app}\packages\requirements_cp311 -r {app}\packages\requirements.txt"; StatusMsg: "Installing Python dependencies (this may take a few minutes)..."; Flags: waituntilterminated

; 4. 配置安装参数（用户输入LLM设置）- 自动弹出，必须执行
Filename: "{app}\config_setup.bat"; Parameters: "{app}"; Description: "Configure LLM settings"; StatusMsg: "Launching configuration wizard..."; Flags: shellexec waituntilterminated; WorkingDir: "{app}"

; 5. 检查安装状态
Filename: "{app}\check_integrity.bat"; Description: "Verify installation"; StatusMsg: "Verifying installation..."; Flags: postinstall shellexec skipifsilent unchecked; WorkingDir: "{app}"

; 6. 显示 README
Filename: "{app}\README.md"; Description: "View README"; Flags: postinstall shellexec skipifsilent unchecked

; 7. 启动 Web 界面（可选）
Filename: "{app}\start_all.bat"; Description: "Start services now"; Flags: postinstall shellexec skipifsilent unchecked; WorkingDir: "{app}"

[UninstallDelete]
; Clean up logs and cache
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\python_embedded\Lib\site-packages"

[Code]
// 卸载时询问是否保留用户数据
function InitializeUninstall(): Boolean;
begin
  if MsgBox('Do you want to keep your documents folder (user data)?', mbConfirmation, MB_YESNO) = IDYES then
    Result := True
  else begin
    DelTree(ExpandConstant('{app}\documents'), True, True, True);
    Result := True;
  end;
end;