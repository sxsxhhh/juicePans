# 网盘类型标识（统一口径）

对外命令一律用左列。海搜内部代码不同，脚本会自动映射。

| 标识 | 名称 | 海搜代码 |
|---|---|---|
| `baidu` | 百度网盘 | `baidu` |
| `aliyun` | 阿里云盘 | `ali` |
| `quark` | 夸克网盘 | `quark` |
| `xunlei` | 迅雷网盘 | `xunlei` |
| `uc` | UC网盘 | `uc` |
| `115` | 115 网盘 | `115` |
| `mobile` | 移动云盘 | `yidong` |
| `tianyi` | 天翼云盘 | `tianyi` |
| `123` | 123 网盘 | `123` |
| `pikpak` | PikPak | （无） |
| `guangya` | 光鸭云盘 | （无） |
| `lanzou` | 蓝奏云 | （无） |
| `magnet` | 磁力链接 | （无） |
| `ed2k` | 电驴 | （无） |

别名：`ali` / `alipan` → `aliyun`；`yidong` → `mobile`。

链接检测（v1.6.0 起内置 8 类匿名核验）：夸克链接优先夸克 CLI 实测（需 `QUARK_SKILL_DIR` + `NODE_BIN`），CLI 缺席时走内置匿名接口兜底；阿里/115/123/天翼/百度/蓝奏/UC 由 `check_links.py` 内置匿名检测；其次自建 PanSou（`PANSOU_URL` / `:8888`）；迅雷/移动/PikPak/磁力/电驴不检测（磁力/电驴永不误伤），标「未核验」不假装核验。影视库接口只返回百度、夸克。
