# juicePans：网盘/盘搜聚合项目补充调研

> 调研日期：2026-09-16（UTC+8）。通过 GitHub MCP `search_repositories`、`get_file_contents` 及 WebSearch 检索；未克隆任何仓库。Stars 是检索时的公开快照，`—` 表示未取得可靠数值。
>
> 已知项目（题目所列）不计入下表；下表只列 NEW 项目。需要注意：其中部分是前端、客户端、适配器或二开版本，不应误当作新的独立搜索引擎。

## 结论先行

最值得优先拆解：

1. **ucmao/pan-relay**：搜索聚合、私有资源库、自动转存/链接替换、开放 API 的完整闭环。
2. **Silent1566/PansouAndPanCheck**：在搜索 API 后置链接测活，直接对应“结果质量”问题。
3. **NDFour/pansou-rust**：兼容 PanSou API，带缓存、插件、可选落库和测试，适合研究轻量引擎边界。
4. **dszz453/pansou-edge**：Cloudflare Workers/KV、原生 TG 抓取、插件兼容、测活和过期缓存兜底。
5. **fish2018/pansou-web**：可直接借鉴 Docker、插件/频道配置、缓存、认证和多架构发布的产品化方式。
6. **dyboy2017/pansousou**：老式“爬取→入库→全文检索”链路，适合作为历史方案和失效风险反例。

## NEW 候选（30 个）

| owner/repo | Stars | 一句话做什么 | Verdict | 为什么 |
|---|---:|---|---|---|
| [joyce677/panhub](https://github.com/joyce677/panhub) | — | PanHub 聚合多个资源站和公开频道，覆盖阿里、夸克、百度、115、迅雷等。 | 可借鉴引擎 | 与 juicePans 目标最接近；重点看优先频道、并发、暂停/继续、LRU 缓存和结果去重。需核对与已知 PanHub 项目的代码/派生关系。 |
| [misiai/hunhepan](https://github.com/misiai/hunhepan) | 278 | Android 混合盘，聚合约 20 个百度/阿里/夸克网盘源及磁力搜索。 | 可借鉴思路 | 多源统一展示、网盘/磁力并列和移动端交互值得参考；Android 客户端形态不宜直接作为网站底座。 |
| [fish2018/pansou-web](https://github.com/fish2018/pansou-web) | 340 | PanSou 的前后端镜像集成版，Docker 一键运行，带频道、插件、缓存和认证配置。 | 可借鉴引擎 | 是成熟的部署/UI 包装层，适合参考 juicePans 的容器化、配置项、多架构和 API 鉴权；核心搜索能力仍依赖 PanSou。 |
| [eKing-one/pansou](https://github.com/eKing-one/pansou) | 113 | ThinkPHP + MySQL 网盘搜索站，支持批量导入、链接管理、失效检测和热搜词。 | 可借鉴引擎 | 对“自有资源索引库”很有参考价值：导入、排序、分类、失效检测和后台运营功能齐全；PHP/MySQL 技术栈需另行迁移。 |
| [dyboy2017/pansousou](https://github.com/dyboy2017/pansousou) | 126 | 采集网盘链接写入 MySQL，再提供 PHP Web 关键词搜索；公开过大规模历史数据方案。 | 可借鉴思路 | 展示了离线索引和简单搜索的最小闭环；README 明确指出目标站点接口/反爬已变化，不能照搬在线爬取。 |
| [ucmao/pan-relay](https://github.com/ucmao/pan-relay) | 70 | Python/Flask 多网盘聚合中继：本地资源库、第三方 API、TG/插件搜索，并支持转存后替换分享链接。 | 可借鉴引擎 | 最接近“聚合搜索+自有资源优先”的业务闭环；SQLite、开放 JSON API、动态搜索源和多网盘凭证管理都值得拆解。自动转存涉及账号风控，建议只借鉴架构。 |
| [ananyou520/Resource-Collection](https://github.com/ananyou520/Resource-Collection) | 72 | Vue 全栈网盘资源分享/采集系统，支持小程序、H5、App、自动采集、转存和分享。 | 可借鉴引擎 | 可参考多端复用、定时采集、资源运营和转存流程；项目明显偏“拉新/收益”场景，网站定位和合规风险较高。 |
| [Silent1566/PansouAndPanCheck](https://github.com/Silent1566/PansouAndPanCheck) | 54 | Pansou API 的代理层，增加多网盘链接有效性检测、过滤、统计和认证。 | 可借鉴引擎 | 对 juicePans 最有用的是“搜索后测活”质量层：兼容原 API、批量检测、JWT、过滤统计，可作为独立后处理服务。 |
| [759039446/OnePanSearchApi](https://github.com/759039446/OnePanSearchApi) | 52 | FastAPI/aiohttp 聚合多个网盘资源站，按网盘类型、来源站点和分页返回统一 JSON。 | 可借鉴引擎 | 适合参考插件/来源适配器接口、统一字段、分页及异步并发；README 也暴露了来源站点变更和正则脆弱性。 |
| [NDFour/pansou-rust](https://github.com/NDFour/pansou-rust) | 4 | Rust + Axum 的 TG/云盘聚合搜索，兼容 PanSou API，带缓存、插件、可选 SQLite 落库和测试。 | 可借鉴引擎 | 代码规模小但架构清晰：并发搜索、TTL、后置落库、健康检查、链接检测接口和单元测试，适合做高性能替代实现。 |
| [dszz453/pansou-edge](https://github.com/dszz453/pansou-edge) | 0 | Cloudflare Workers/KV 原生 TG 抓取聚合，支持 PanSou 兼容插件、自定义 REST、测活和过期缓存兜底。 | 可借鉴引擎 | 对无服务器部署很有价值：频道分片、插件单独调用、KV 配置、WAF 重试、stale-while-error 和链接分类/测活。注意 Workers 在中国大陆网络可达性。 |
| [Cole404/DBPanso](https://github.com/Cole404/DBPanso) | — | Chromium 侧边栏扩展：从豆瓣影片标题搜索 Telegram 公开频道并聚合网盘链接。 | 可借鉴思路 | “上下文页面一键搜”是 juicePans 可做的浏览器入口；本地解析、去重、排序和频道配置值得借鉴，但受浏览器跨域、Telegram 限流和豆瓣场景限制。 |
| [Xwudao/reman-app-release](https://github.com/Xwudao/reman-app-release) | 5 | ReMan 网盘搜索 App 的构建/发布仓库。 | 可借鉴思路 | 可参考移动端搜索结果、资源分类和发布流水线；它主要是构建产物/发布仓，不是独立搜索后端。 |
| [chenggaofeng/pansou-search-engine](https://github.com/chenggaofeng/pansou-search-engine) | 8 | PanSou 相关的多平台搜索、PWA 和资源集合管理前端/应用。 | 可借鉴思路 | 可参考 PWA、收藏/资源集合和搜索结果管理；与 PanSou 生态耦合，不能视作新的采集引擎。 |
| [hugiot/pansou-fpk](https://github.com/hugiot/pansou-fpk) | 8 | 将 PanSou 打包成飞牛 fnOS 应用。 | 可借鉴思路 | 可借鉴 NAS 一键安装、服务编排和持久化配置；功能主要是发行适配，新增搜索能力有限。 |
| [VC-share/vcsoso-QuarkShare](https://github.com/VC-share/vcsoso-QuarkShare) | 32 | 夸克影视资源分享/搜索站，按日发布 1080P/4K 影视资源。 | 可借鉴思路 | 可参考影视资源卡片、标签、更新流和 SEO 内容组织；更像垂直内容站，采集/运营及版权风险使其不宜直接作为公共网站方案。 |
| [3078363489/Quark_Magnet_Search](https://github.com/3078363489/Quark_Magnet_Search) | 14 | 磁力搜索引擎，带采集 API、夸克智能转存/缓存、SEO、站点地图和统计。 | 可借鉴思路 | 可借鉴磁力与网盘混合结果、缓存、SEO 和统计埋点；“自动转存”与内容分发需要严格控制。 |
| [aidup/api-so](https://github.com/aidup/api-so) | 16 | PHP 单页聚合 API/搜索，覆盖阿里、夸克及影视/4K 资源。 | 可借鉴思路 | 适合作为轻量前端对接层和 API 聚合思路参考；描述信息较少，需审查实际来源稳定性与代码质量。 |
| [sunwang115/baozang-search](https://github.com/sunwang115/baozang-search) | 8 | Python 网盘搜索源码，宣称覆盖 17 种网盘并支持转存分享接口。 | 可借鉴思路 | 可参考多网盘适配矩阵和统一转存抽象；项目较新且星数少，凭证/接口维护成本高，建议只做原型研究。 |
| [guhua0521/guhua-xinyue-search](https://github.com/guhua0521/guhua-xinyue-search) | 9 | 心悦搜索二开网盘站，支持夸克、百度、阿里、UC、迅雷等并可开分站。 | 不适合网站 | 有多网盘和分站运营思路，但属于二开/商业化分发取向；重复建设多，依赖原系统和接口，复用价值低。 |
| [cq797716/xinyue-search](https://github.com/cq797716/xinyue-search) | 20 | 基于心悦搜索二开的夸克资源管理系统，支持一键转存分享。 | 不适合网站 | 与已知心悦项目高度重复，主要价值是了解转存/资源管理产品形态；不建议作为 juicePans 独立引擎来源。 |
| [wangsy116/panso](https://github.com/wangsy116/panso) | 4 | panso 网盘搜索引擎源码，覆盖百度、阿里、夸克、迅雷。 | 可借鉴思路 | 可做兼容性对照和最小搜索站样本；文档与社区信号弱，适合阅读接口/数据模型，不建议直接生产部署。 |
| [jiajiaso-loey/jiajiaso-loey](https://github.com/jiajiaso-loey/jiajiaso-loey) | 3 | “珈珈搜索”脚本，统一搜索百度、夸克、阿里、迅雷、UC、天翼、115、123 等。 | 可借鉴思路 | 网盘域名识别和来源编排可供参考；星数低、维护状态有限，且依赖外部站点，适合提取正则/字段设计。 |
| [midoujia/wangpansearch](https://github.com/midoujia/wangpansearch) | 2 | Java 8/Spring Boot + Elasticsearch 的百度/阿里/夸克搜索系统。 | 可借鉴引擎 | 对 juicePans 的索引层有参考价值：ES 全文检索、后端 API 和前端分离；年代/活跃度一般，需验证依赖和数据导入链路。 |
| [2182977liu-bit/quark-search](https://github.com/2182977liu-bit/quark-search) | 1 | Flask + SQLite + Docker 的轻量夸克资源搜索引擎。 | 可借鉴思路 | 可作为单网盘 MVP、容器化和 SQLite schema 的参考；单源能力不足以支撑聚合网站。 |
| [scenlinx/panws.net](https://github.com/scenlinx/panws.net) | 1 | “盘万搜”聚合百度、迅雷、阿里、夸克资源的站点源码。 | 可借鉴思路 | 可参考多网盘入口和结果卡片；仓库信息少、星数低，优先当作 UI/站点结构样本，不宜作为核心引擎。 |
| [ghost-guest/quark_baidu_pansou](https://github.com/ghost-guest/quark_baidu_pansou) | 5 | 百度和夸克资源搜索，并尝试转存/分享。 | 需自建跳过 | 方向贴近但规模和维护信号弱，且转存依赖账号凭证；除非明确要做双盘自动化，否则不值得增加维护面。 |
| [maomao19950101/ResourceSearch](https://github.com/maomao19950101/ResourceSearch) | 0 | Kotlin 资源搜索 App，聚合 8 个搜索引擎和网盘搜索。 | 可借鉴思路 | 可参考移动端聚合搜索、统一结果模型和入口设计；没有足够社区验证，不能直接承担网站后端。 |
| [gaozhangmin/boxplayer](https://github.com/gaozhangmin/boxplayer) | 6,928 | 多平台云盘/本地媒体库管理器，提供跨云盘统一搜索、媒体整理和 AI/播放器能力。 | 可借鉴思路 | 不是公共网盘资源聚合站，但跨盘索引、账号管理、媒体元数据、统一搜索和 MCP/CLI 设计很适合 juicePans 的“个人库”方向。 |
| [laoma2053/awesome-zhuiju-free](https://github.com/laoma2053/awesome-zhuiju-free) | 8,635 | 维护免费追剧资源指南，收录网盘搜索、磁力、字幕、TVBox/IPTV 等入口并持续检查。 | 可借鉴思路 | 不是搜索引擎源码，但“目录/导航 + 可用性维护 + 分类标签”的内容运营模式值得参考；不适合直接作为检索后端。 |

## 按 juicePans 的落地优先级

- **优先读引擎/服务代码**：`ucmao/pan-relay`、`Silent1566/PansouAndPanCheck`、`NDFour/pansou-rust`、`dszz453/pansou-edge`、`fish2018/pansou-web`、`759039446/OnePanSearchApi`、`eKing-one/pansou`。
- **优先读产品交互/入口**：`joyce677/panhub`、`Cole404/DBPanso`、`misiai/hunhepan`、`gaozhangmin/boxplayer`。
- **只提取局部思路**：`dyboy2017/pansousou`、`midoujia/wangpansearch`、`2182977liu-bit/quark-search`、`laoma2053/awesome-zhuiju-free` 等。
- **建议跳过或仅做对照**：心悦二开、纯发行包、低活跃的自动转存/凭证型项目；它们通常不是新的搜索核心，且会引入账号封禁、接口漂移和版权/合规风险。

## 研究边界

- 本表只基于公开仓库元数据和 README 级内容，不代表对每个项目做了运行验证。
- 未克隆仓库、未登录第三方网盘、未使用任何账号凭证。
- 资源搜索/自动转存可能涉及服务条款、版权和隐私问题；juicePans 更适合聚合公开可访问结果、做去重/排序/测活，并保留来源与审计信息。
