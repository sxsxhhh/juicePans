# 果汁搜盘（juicePans 绿色版）

本地、便携的多源公开网盘搜索站点。仅依赖 **Python 3 标准库**，无需 Docker、无需安装第三方包。

> 新手请先看同目录下的 **`使用说明.txt`**（记事本直接打开即可）。
>
> 加微信备注进交流群：**sxsxhh2**

## 快速开始（Windows）

1. 安装 Python 3.10+，安装时勾选 **Add python.exe to PATH**。
2. 解压后进入 `juicePans` 文件夹，双击 **`start.bat`**。
3. 保持黑色命令行窗口不要关；约 2 秒后浏览器会打开 `http://127.0.0.1:8765/`。
4. 用完后直接关闭该黑窗口即可停止服务。

若黑窗口一闪就关：多半是未安装 Python 或未加入 PATH，请按上面第 1 步重装后再试。

## 快速开始（Linux / macOS）

```bash
chmod +x start.sh
./start.sh
```

或：

```bash
python3 server.py
# 浏览器访问 http://127.0.0.1:8765/
```

## 页面怎么用

- 输入关键词搜索；上方 Tab 可按网盘类型筛选（夸克 / 百度 / 阿里等）。
- 引擎默认盘搜、小云、海搜；可选盘小子、TG 库。
- 结果一律标记为「公开检索（未核验）」——请自行核验后再使用。
- 破解、色情、赌博类关键词会被拒绝。

## 常见问题

| 现象 | 处理 |
|------|------|
| `start.bat` 一闪就关 | 安装 Python 并勾选 Add to PATH；或在本目录运行 `python server.py` 看报错 |
| 打不开网页 | 确认黑窗口仍在；手动访问 http://127.0.0.1:8765/ |
| 端口被占用 | 关掉旧窗口，或设置 `JUICEPANS_PORT=8766` 后重启 |
| 搜不到结果 | 换关键词 / 换网盘 Tab；需能访问外网公开源 |

## API（可选）

```
GET /api/search?q=关键词&clouds=quark,baidu&engines=pansou,yunso,haisou
GET /api/health
```

- `clouds` 为空 = 综合全部；`quark,baidu` 会映射为对应网盘类型。
- `engines` 默认 `pansou,yunso,haisou`，可含 `panxiaozi`、`ghspider`。

## 目录结构

```
juicePans/
  使用说明.txt       # 新手操作指南（优先阅读）
  start.bat / start.sh
  server.py          # HTTP 服务（stdlib）
  search_core.py     # 多源搜索核心（stdlib）
  static/            # 前端
  docs/github-research.md
  README_zh.md
```

## 环境变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `JUICEPANS_HOST` | `127.0.0.1` | 监听地址 |
| `JUICEPANS_PORT` | `8765` | 端口 |

## 免责声明

本工具仅聚合公开可访问的检索结果，不存储网盘账号，不对链接有效性、版权归属做保证。请合法合规使用。
