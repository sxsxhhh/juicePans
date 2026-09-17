# 绿色版（解压即用）使用教程

绿色版是把本地 Web 站点打成的便携压缩包：解压 → 双击启动 → 浏览器搜索。适合不想装 Docker、也不想当 AI Skill 用的同学。

## 下载

到仓库 [Releases](https://github.com/sxsxhhh/juicePans/releases) 下载附件，文件名类似：

`juicePans-*-web-green.zip`

## Windows

1. 解压到任意文件夹（路径尽量不要含奇怪权限限制）
2. 确认本机已安装 **Python 3.8+**，安装时勾选 **Add python.exe to PATH**
3. 双击 `start.bat`
4. 浏览器打开 `http://127.0.0.1:8765/`（脚本一般会自动打开）
5. 输入关键词搜索；可勾选引擎；需要时可打开「检验链接存活」
6. 搜索过慢时会出现「终止」按钮，可立刻中断
7. 关掉黑色命令行窗口即停止服务

## macOS / Linux

```bash
unzip juicePans-*-web-green.zip
cd juicePans-web-green   # 以实际解压目录名为准
bash start.sh
# 或: python3 server.py
```

浏览器访问 `http://127.0.0.1:8765/`。

## 局域网（手机访问）

默认只监听本机。需要手机同网访问时：

```bash
export JUICEPANS_HOST=0.0.0.0
export JUICEPANS_PORT=8765
python3 server.py
```

Windows PowerShell：

```powershell
$env:JUICEPANS_HOST="0.0.0.0"
$env:JUICEPANS_PORT="8765"
python server.py
```

然后用 `http://<电脑局域网IP>:8765/` 打开。

## 和 Skill / Docker 的区别

| 方式 | 适合谁 | 入口 |
|------|--------|------|
| AI Skill 压缩包 | 装到 Cursor / Codex 等对话里搜 | Releases 里的 `*-skill.zip` |
| 绿色版 Web | 浏览器本地搜 | Releases 里的 `*-web-green.zip` |
| Docker | 服务器 / 玩客云 7×24 | 见 [deploy-docker.md](./deploy-docker.md) |
| 源码本地跑 | 开发调试 | 见 [deploy-local.md](./deploy-local.md) |

## 常见问题

- **start.bat 闪退**：未安装 Python 或未加入 PATH。
- **端口被占用**：设置 `JUICEPANS_PORT` 换端口。
- **TG 库无结果**：该源常访问 GitHub，网络受限时可取消勾选，改用其他引擎。
- **只要转存**：本绿色版只搜索展示，不转存；请用独立转存工具。
