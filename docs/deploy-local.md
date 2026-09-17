# 本地 Web 部署（果汁搜盘站点）

本仓库 `web/` 目录是浏览器可用的本地搜盘站点（独立于 AI Skill 的 CLI/`scripts/`）。

## 环境

- Python 3.10+（推荐 3.12）
- 仅标准库 + 站点自带脚本，无需额外 pip 包（若你本地改过依赖以实际为准）

## 启动

```bash
cd web
# 仅本机访问（默认）
python3 server.py

# 局域网可访问（手机/其他电脑）
# Linux / macOS
export JUICEPANS_HOST=0.0.0.0
export JUICEPANS_PORT=8765
python3 server.py

# Windows PowerShell
$env:JUICEPANS_HOST="0.0.0.0"
$env:JUICEPANS_PORT="8765"
python server.py
```

也可使用：

- Windows：双击 `web/start.bat`
- Linux/macOS：`bash web/start.sh`

浏览器打开：`http://127.0.0.1:8765/`  
局域网：`http://<主机局域网IP>:8765/`

## 功能摘要

- 多盘种并行搜索、去重与相关度排序
- 「检验链接存活」开关（可隐藏失效链接）
- 搜索过慢时可「终止」
- 环境变量：`JUICEPANS_HOST`、`JUICEPANS_PORT`

## 说明

- TG 库等依赖 GitHub 的源，在部分网络环境下可能不可用
- 本站点与「果汁转存」无关；转存请使用独立项目
