# PanSou 自部署 API 参考

供 `search.py --engine local` 与 `check_links.py` 使用。镜像：`ghcr.io/fish2018/pansou:latest`
（上游 `github.com/fish2018/pansou`）。

## Base URL
```
$PANSOU_URL   # 默认 http://localhost:8888
```

## 端点
| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/health` | GET | 否 | 健康检查 |
| `/api/search` | POST/GET | 可选 | 搜索资源 |
| `/api/check/links` | POST | 可选 | 批量验链 |
| `/api/auth/login` | POST | 否 | 登录获取 Token |
| `/api/auth/verify` | POST | 是 | 验证 Token |

## 搜索 API
**Request Body：**
| 参数 | 类型 | 说明 |
|------|------|------|
| `kw` | string | 关键词（必填） |
| `res` | string | **`merge`（默认，推荐）** / `all` / `results` |
| `src` | string | `plugin`（本技能默认，更快更稳）/ `all` / `tg` |
| `cloud_types` | string[] | 网盘类型过滤（见下） |
| `channels` | string[] | TG 频道 |
| `plugins` | string[] | 指定插件 |
| `filter` | object | `{"include":[...],"exclude":[...]}` |
| `refresh` | bool | 强制刷新缓存 |

> **纠错**：原 netdisk `search.py` 用 `res:"all"` 却按 `merged_by_type` 解析，导致有时显示
> "无结果"。统一用 `res:"merge"`，响应顶层即含 `merged_by_type`（按平台分组的数组）。

**Response（res=merge）：**
```json
{
  "total": 15,
  "merged_by_type": {
    "quark": [{"url":"https://pan.quark.cn/s/xxx","password":"","note":"标题","datetime":"...","source":"plugin:labi"}]
  }
}
```

## 验链 API
`POST /api/check/links`
```json
{"items":[{"disk_type":"quark","url":"https://pan.quark.cn/s/xxx"},
          {"disk_type":"baidu","url":"https://pan.baidu.com/s/yyy","password":"1234"}]}
```
支持检测类型：`baidu, aliyun, quark, tianyi, uc, mobile, 115, xunlei, 123`
state：`ok`(有效) / `bad`(失效) / `locked`(需码/码错) / `unsupported` / `uncertain`

注意：以上是 PanSou 接口单次返回的原始状态。`check_links.py` 的**本地四级状态机**（v1.4.0）会把它转成跨次状态：`ok`(有效) / `suspect`(疑似失效，首败) / `bad`(确认失效，连续 2 次失败) / `uncertain`(未核验)——汇报时以脚本输出为准。

## 支持的网盘类型（标准化，共 14 类）
`baidu` `aliyun` `quark` `tianyi` `uc` `mobile` `115` `pikpak` `xunlei` `123`
`magnet` `ed2k` `guangya`(光鸭) `others`

## 部署
```bash
docker run -d --name netdisk-search -p 8888:8888 --restart unless-stopped ghcr.io/fish2018/pansou:latest
curl http://localhost:8888/api/health
export PANSOU_URL=http://localhost:8888
```
启用认证：容器侧 `AUTH_ENABLED=true` + `AUTH_USERS=user:pass`。（本技能脚本未实现登录握手，若开启认证请在网关层放行。）
