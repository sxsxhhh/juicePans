# 数据源

## 脚本引擎

**本沙箱实测**列基于 WorkBuddy 沙箱 2026-09-15 实跑结果。

| 引擎 | 默认？ | 地址 | 说明 | 本沙箱实测 |
|---|---|---|---|---|
| `pansou` | 是 | `https://so.252035.xyz/api/search` | 公开盘搜；公开站先 GET（有 include/exclude 时先 POST）。响应可能是裸 `merged_by_type` 或 `{code:0,data:...}` | ✅ GET 可用（返真实 `merged_by_type`）；`POST` 超时/被代理改坏 → 已默认 GET 优先 |
| `haisou` | 是 | `https://haisou.cc/api/v2/shares/search` | 不要传 `platforms:["all"]`（会 422）。链接验证耗积分，默认不做 | ⚠️ 可用但常 429（共享出口 IP 限流）；单源失败不中断 |
| `yunso` | 是 | `https://www.yunso.net/api/opensearch.php` | `wd` + `mode`（90001 智能 / 90002 精准）；直链在 `Data[].Scrurl` | ✅ 可用（JSON、真实直链、带时间） |
| `panxiaozi` | 否 | `https://pan.xiaozi.cc/resource?q=<kw>` | 盘小子：SSR 搜索页 ld+json 拿资源列表 → 并发抓详情页提取网盘直链 + 简介/分类/更新时间（v1.3.0 新增，来源 [towelong/panxiaozi](https://github.com/towelong/panxiaozi)，官方亦有 Agent Skill） | ✅ 可用（实测「庆余年」6 条夸克直链）；详情页偶发失败会显式报错 |
| `ghspider` | 否 | `https://api.github.com/repos/John-h-netdisk/netdisk-spider/contents/data` | netdisk-spider：TG 频道爬虫聚合库，仓库每 6 小时自动更新 JSON；引擎拉最新文件本地过滤（v1.3.0 新增，来源 [John-h-netdisk/netdisk-spider](https://github.com/John-h-netdisk/netdisk-spider)） | ✅ 可用（仅百度/夸克两类，数据量约 4 千条）；GitHub API 匿名限流 60 次/时，够用 |
| `movie` | 否 | `https://meng-ge.top/api/movieData/getMoviesByType` | 影视库引擎；需显式 `--engine movie` | ❌ 502（域名被沙箱代理拦）；仅显式指定时尝试 |
| `local` | 否 | `PANSOU_URL` / `NETDISK_API_URL` / `http://127.0.0.1:8888` | 自建 PanSou。`all` **不含**此项 | 取决于是否部署；有则 `/api/health` 探活 |

`--engine all` = `pansou,haisou,yunso`（本版不含 `movie` / `local` / `panxiaozi` / `ghspider`，后两者需显式指定）。

## 自建 PanSou（可选）

上游：<https://github.com/fish2018/pansou>

```text
docker run -d --name netdisk-search -p 8888:8888 --restart unless-stopped ghcr.io/fish2018/pansou:latest
```

健康检查：`http://127.0.0.1:8888/api/health`。链接检测：`POST /api/check/links`。没有检测接口就不要编造有效/无效。（容器若开认证需在网关层放行；本技能脚本未实现登录握手。）

## GitHub 同类项目评估（2026-09-16 三轮：首轮用户提交 7 仓库；次轮调研 4 个热门项目；第三轮再读 11 个（6+5）并合入借鉴要点）

整合准入门槛：公开 HTTP 接口可直接调用 / 无登录墙 / 不违反站点使用条款 / 纯标准库可实现。

| 仓库 | 结论 | 说明 |
|---|---|---|
| [towelong/panxiaozi](https://github.com/towelong/panxiaozi) | ✅ **已整合**（`panxiaozi` 引擎） | SSR 搜索页 + 详情页直链；官方自己也出了 Agent Skill，思路一致 |
| [John-h-netdisk/netdisk-spider](https://github.com/John-h-netdisk/netdisk-spider) | ✅ **已整合**（`ghspider` 引擎） | 仓库 data/*.json 即数据集，raw 直拉零门槛 |
| [675061370/xinyue-search](https://github.com/675061370/xinyue-search) | ❌ 不整合 | 心悦搜索：可自部署的 PHP 系统（夸克/百度/阿里/UC/迅雷），**无公开托管 API**；与已接入的 `yunso`（小云搜索）同属一类数据源，暂无增量接口 |
| [wu529778790/panhub.shenzjd.com](https://github.com/wu529778790/panhub.shenzjd.com) | ❌ 不整合 | PanHub：搜索需公众号登录（wx-auth），且 README 明确「不要用脚本或服务端代理转发请求」——违反使用条款，不碰 |
| [jiangrui1994/CloudSaver](https://github.com/jiangrui1994/CloudSaver) | ❌ 不整合 | 需 Docker 自建（新版闭源，仓库停在 V0.2.5）；搜索走 TG 订阅 + 网盘 Cookie 转存型，与「只搜不转存」定位不符 |
| [caixiaoq/DuPanSou-Archive（supansou）](https://github.com/caixiaoq/DuPanSou-Archive) | ❌ 不整合（已覆盖），**思路已借鉴**（v1.4.0） | 本质是 PanSou 的增强壳（SQLite 索引 + 链接四级状态机 + 豆瓣榜单）；果汁搜盘（juicePans）已支持 `PANSOU_URL` 自建 PanSou，等价能力。其「链接四级状态机」已移植进 `check_links.py`（四级判定 + 连续 2 次判死 + 72h/30min/12h 复检策略，状态存本地 JSON） |
| [fish2018/pansou](https://github.com/fish2018/pansou) | ✅ 已支持（`local` 引擎 / `PANSOU_URL`），**思路已借鉴**（v1.5.0） | 约 8k★、持续维护的同类头部项目；「插件等级 + 时间新鲜度 + 关键词匹配度」综合排序已实现为合并去重后的组内排序 |
| [wu529778790/panhub.shenzjd.com](https://github.com/wu529778790/panhub.shenzjd.com) | ❌ 不整合（wx-auth 登录墙仍在），**思路已借鉴**（v1.5.0） | 现已开源（1.6k★）：插件熔断、链接探活、CJK 关键词变体、fetchWithRetry——熔断与变体重试已移植，详情页抓取加重试 |
| [huanyu-a/panseek](https://github.com/huanyu-a/panseek) | ❌ 不整合（须自建 Nuxt 4 + Workers 全栈），**思路已借鉴**（v1.5.0） | PanHub 分支：140+ TG 频道 / 68 插件 / 优先级调度；13 类网盘域名表已并入 URL 识别（anxia / 123 多域名 / mypikpak / guangyapan） |
| [Maishan-Inc/Limitless-search](https://github.com/Maishan-Inc/Limitless-search) | ❌ 不整合（须自建 PostgreSQL 全栈） | 101 TG 频道 + 61 插件 + AI 联网搜索；「榜单 / 搜索建议」发现入口思路已化为流程第 1 步指引 |
| [Xwudao/lzpan_search](https://github.com/Xwudao/lzpan_search) | ❌ 不整合 | 懒盘搜索：2020 年的前端壳项目，数据源为爬各站接口，近年基本停滞；与黑名单中 SPA 站同类 |
| [fish2018/NetDiskLinkValidator](https://github.com/fish2018/NetDiskLinkValidator) | ❌ 不整合（单文件参考实现），**要点已合入**（v1.6.0） | 单文件 8 类网盘匿名检测器；阿里/115/123/天翼/百度/蓝奏/UC 检测端点与判定关键词已移植进 `check_links.py`（全标准库、无 cookie） |
| [owu/share-sniffer](https://github.com/owu/share-sniffer) | ❌ 不整合（Go 预编译 + GPL v3），**思路已借鉴**（v1.6.0） | 9 类网盘批量失效检测 CLI/Docker API；仅借鉴「统一状态码 + 检测耗时」输出契约，未接其外部接口（契约未逐条验证） |
| [Shiwen645/Network_disk_resource_detection](https://github.com/Shiwen645/Network_disk_resource_detection) | ❌ 不整合 | Flask 自建检测 API；蓝奏检测思路已随 NetDiskLinkValidator 一并覆盖 |
| [Cp0204/quark-auto-save](https://github.com/Cp0204/quark-auto-save) | ❌ 不整合（转存生态，与「只搜不转存」定位不符），**要点已合入**（v1.6.0） | 3k★ 夸克自动转存；「记录失效分享并跳过」→ `search.py` 对状态机确认失效的链接自动沉底 |
| [Xwudao/go-pansearch-release](https://github.com/Xwudao/go-pansearch-release) | ❌ 不整合（须自建 Elasticsearch + Redis） | PanSearch：ES 全文搜索 + 热词/搜索建议；属输入侧体验，对 CLI 脚本价值低，不采纳 |
| [Xwudao/pan](https://github.com/Xwudao/pan) | ❌ 不整合 | ReMan-lite：二进制自建引擎带后台；热词记录与 PanSearch 重叠，参考价值低，备查 |
| [farfarfun/funresource](https://github.com/farfarfun/funresource) | ❌ 暂不整合（备查） | pip 即用的聚合采集入库（RSS/TG → 打标签 → SQLite 去重）；「采集→本地检索」模式与 RSS 来源是未来新引擎候选，改动大，本轮不展开 |
| [fancydirty/mediary-scout](https://github.com/fancydirty/mediary-scout) | ❌ 不整合（转存型，与定位不符），**思路已借鉴**（v1.6.0） | 1401★ LLM Agent 网盘影视库；「选最佳匹配」评估维度已化为展示指引；其索引器抽象印证 `PANSOU_URL` 可插拔设计 |
| [OzoO0/cloud-auto-save-x](https://github.com/OzoO0/cloud-auto-save-x) | ❌ 不整合（转存型），**思路已借鉴**（v1.6.0） | CASX：10 网盘自动追更转存；「链接失效自动换链」→ 交付前补搜指引；UC/光鸭一等公民覆盖与 cloud-types 口径一致 |
| [odysseusmax/tg-index](https://github.com/odysseusmax/tg-index)（含 enhanced fork） | ❌ 不整合（需 TG 账号自建），**要点已合入**（v1.6.0） | TG 频道索引 Web 应用；enhanced 的 FloodWait 指数退避 + 限流已移植进 `ghspider` 引擎 |
| [ziaocunhuo/qilin-Auto](https://github.com/ziaocunhuo/qilin-Auto) | ❌ 不整合 | 影视库自动化平台，与搜索交集极小，备查 |

## 不要做的

- 深度页面爬虫（cloudscraper / 并发抓站）
- 把下表网页站当脚本引擎
- 假地址 `netdisk-search.example.com`、`uv` / `requests` 硬依赖、写死 Linux 家目录
- 把 Hermes / OpenClaw 安装说明当必装步骤

## 网页搜索站测评（2026-09-15，Cursor 与 WorkBuddy 独立复测结论一致）

判定：普通 HTTP 拿到网盘直链才进脚本。SPA / 校验 / 中间页 / 证书挂了就不爬。下表 15 站即用户整理提交的一批，
**两版均判定不可直接接入**（普通 HTTP 拿不到直链），按用户要求本版暂不纳入。

| 站 | 结论 | 原因 |
|---|---|---|
| 混合盘 hunhepan.com | 不加 | `POST /open/search/disk` 有 JSON，但本沙箱握手失败、实测 0 条，精修时已移除 |
| 爱搜 esoua.com | 不加 | 前端壳，无直链 |
| 橘子盘搜 nmme.icu | 不加 | 跳 nmme.one 后 404 |
| 懒盘 lzpanx.com | 不加 | SSL 握手超时 |
| 盘搜 panso.pro | 不加 | 前端壳 |
| 帕卡 cuppaso.com | 不加 | 站内 `share/数字:token`，不是网盘 URL |
| 盘搜搜 / 小白盘 zhiso.cc | 不加 | **同一 URL**；JWT 跳转 |
| 搜网盘 zhongchuangwl.com | 不加 | `/tag/关键词/` 404 |
| 夸克探宝 quarkfinder.top | 不加 | 403 / Cloudflare |
| 夸克盘搜索 pansosuo.com | 不加 | 校验页 |
| 夸克搜 qkpanso.com | 不加 | 前端壳 |
| 毕方铺 iizhi.cn | 不加 | 证书过期 / 502 |
| 云盘吧 yunpan8.net | 不加 | 浏览器检查页 |
| 奇乐搜 qileso.com | 不加 | Cloudflare |
| 爱盘搜 aipanso.com | 不加 | Cloudflare + JS 加密 + `/s/` 中间页 + 同意声明 |
