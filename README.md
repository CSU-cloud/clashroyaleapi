# Clash Royale API 完整工具集

一个功能完善的 Clash Royale（皇室战争）API Python 客户端，提供玩家查询、部落分析、数据统计、排行榜和数据导出等功能。

## ✨ 功能特性

### 🎮 核心功能
- **玩家管理**: 查询玩家信息、战斗日志、宝箱循环
- **部落管理**: 部落信息、成员列表、战争日志、当前战争
- **卡牌数据**: 获取所有卡牌信息
- **锦标赛**: 搜索和查询锦标赛详情
- **排行榜**: 全球/地区玩家和部落排名

### 📊 高级功能
- **数据分析**: 玩家胜率统计、常用卡牌分析、部落实力评估
- **数据导出**: 支持 JSON 和 CSV 格式导出
- **缓存机制**: 自动缓存 API 响应，减少请求次数
- **配置管理**: 支持环境变量和配置文件
- **错误处理**: 完善的异常处理和错误提示

## 🚀 快速开始

### 1. 获取 API Key

1. 访问 [Clash Royale Developer Portal](https://developer.clashroyale.com/)
2. 注册/登录 Supercell 账号
3. 创建 API Key（需要绑定 IP 地址）

### 2. 安装依赖

```bash
pip install requests
```

### 3. 配置 API Key

**方式 1: 环境变量（推荐）**
```bash
# Linux/macOS
export CLASH_ROYALE_API_KEY='your_api_key_here'

# Windows (Command Prompt)
set CLASH_ROYALE_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:CLASH_ROYALE_API_KEY="your_api_key_here"
```

**方式 2: 直接修改代码**
```python
config = Config()
config.api_key = "your_api_key_here"
```

### 4. 运行

```bash
python clashroyaleapi.py
```

## 📖 使用示例

### 基础用法

```python
from clashroyaleapi import ClashRoyaleAPI, Config

# 初始化
config = Config()
config.api_key = "your_api_key_here"
client = ClashRoyaleAPI(config=config)

# 获取玩家信息
player = client.get_player("#2PP")
print(f"玩家: {player['name']}, 奖杯: {player['trophies']}")

# 获取部落信息
clan = client.get_clan("#2PP")
print(f"部落: {clan['name']}, 成员: {clan['members']}")

# 获取部落成员
members = client.list_clan_members("#2PP")
for member in members[:5]:
    print(f"{member['name']} - {member['trophies']} 奖杯")
```

### 数据分析

```python
# 分析玩家统计
stats = client.analyze_player_stats("#2PP")
print(f"胜率: {stats['recent_win_rate']}")
print(f"常用卡牌: {stats['top_cards']}")

# 分析部落统计
clan_stats = client.analyze_clan_stats("#2PP")
print(f"平均奖杯: {clan_stats['avg_trophies']}")
print(f"Top 玩家: {clan_stats['top_players']}")
```

### 数据导出

```python
# 导出玩家数据到 JSON
client.export_player_to_json("#2PP", "player_data.json")

# 导出部落成员到 CSV
client.export_clan_to_csv("#2PP", "clan_members.csv")

# 导出所有卡牌到 JSON
client.export_cards_to_json("cards.json")
```

### 排行榜查询

```python
# 获取全球玩家排行榜
top_players = client.get_player_rankings(limit=10)
for i, player in enumerate(top_players, 1):
    print(f"{i}. {player['name']} - {player['trophies']} 奖杯")

# 获取全球部落排行榜
top_clans = client.get_clan_rankings(limit=10)
for i, clan in enumerate(top_clans, 1):
    print(f"{i}. {clan['name']} - {clan['clanScore']} 分")
```

### 搜索功能

```python
# 搜索部落
clans = client.search_clans("China", limit=5)
for clan in clans:
    print(f"{clan['name']} - {clan['members']} 成员")

# 搜索锦标赛
tournaments = client.search_tournaments("Weekly", limit=5)
for tournament in tournaments:
    print(f"{tournament['name']} - {tournament['players']} 玩家")
```

## 📁 API 方法列表

### 玩家 API
| 方法 | 说明 |
|------|------|
| `get_player(tag)` | 获取玩家信息 |
| `get_player_upcoming_chests(tag)` | 获取即将获得的宝箱 |
| `get_player_battle_log(tag, limit)` | 获取战斗日志 |

### 部落 API
| 方法 | 说明 |
|------|------|
| `get_clan(tag)` | 获取部落信息 |
| `list_clan_members(tag, limit)` | 获取部落成员 |
| `get_clan_war_log(tag, limit)` | 获取战争日志 |
| `get_clan_current_war(tag)` | 获取当前战争 |
| `search_clans(name, limit)` | 搜索部落 |

### 卡牌 API
| 方法 | 说明 |
|------|------|
| `list_cards()` | 获取所有卡牌 |

### 锦标赛 API
| 方法 | 说明 |
|------|------|
| `search_tournaments(name, limit)` | 搜索锦标赛 |
| `get_tournament(tag)` | 获取锦标赛信息 |

### 排行榜 API
| 方法 | 说明 |
|------|------|
| `get_locations()` | 获取地区列表 |
| `get_player_rankings(location_id, limit)` | 获取玩家排行榜 |
| `get_clan_rankings(location_id, limit)` | 获取部落排行榜 |

### 分析功能
| 方法 | 说明 |
|------|------|
| `analyze_player_stats(tag)` | 分析玩家统计 |
| `analyze_clan_stats(tag)` | 分析部落统计 |

### 导出功能
| 方法 | 说明 |
|------|------|
| `export_player_to_json(tag, filename)` | 导出玩家数据到 JSON |
| `export_clan_to_csv(tag, filename)` | 导出部落成员到 CSV |
| `export_cards_to_json(filename)` | 导出卡牌数据到 JSON |

## ⚙️ 配置选项

```python
from clashroyaleapi import Config

config = Config()
config.api_key = "your_api_key"           # API 密钥
config.base_url = "https://api.clashroyale.com/v1"  # API 基础 URL
config.timeout = 30                       # 请求超时时间（秒）
config.cache_enabled = True               # 启用缓存
config.cache_duration = 300               # 缓存时长（秒）
```

## 🔧 高级功能

### 缓存机制

API 客户端内置缓存功能，可以减少重复请求：

```python
config = Config()
config.cache_enabled = True
config.cache_duration = 300  # 5分钟缓存
```

### 错误处理

```python
try:
    player = client.get_player("#INVALID")
except Exception as e:
    print(f"错误: {e}")
    # 可能的错误：
    # - API 密钥无效或 IP 未授权
    # - 资源不存在
    # - API 请求频率超限
    # - 网络请求失败
```

## 📊 输出示例

### 玩家信息
```
============================================================
  玩家信息: Player123
============================================================
标签: #2PP
等级: 13
奖杯: 5234
最高奖杯: 6123
胜利: 1234
失败: 890
部落: AwesomeClan
竞技场: Ultimate Champion
```

### 数据分析
```
============================================================
  玩家统计分析: Player123
============================================================
当前奖杯: 5234
最高奖杯: 6123
等级: 13
总胜利: 1234
总失败: 890
近期胜率: 62.5% (最近24场)

常用卡牌 (Top 5):
  1. Hog Rider - 使用 18 次
  2. Musketeer - 使用 16 次
  3. Fireball - 使用 15 次
  4. The Log - 使用 14 次
  5. Ice Spirit - 使用 13 次
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 许可证

MIT License

## 🔗 相关链接

- [Clash Royale Developer Portal](https://developer.clashroyale.com/)
- [Official API Documentation](https://developer.clashroyale.com/#/documentation)
- [RoyaleAPI](https://royaleapi.com/)

## ⚠️ 注意事项

1. **API 限制**: 官方 API 有请求频率限制，请合理使用
2. **IP 白名单**: API Key 需要绑定 IP 地址
3. **标签格式**: 玩家和部落标签必须以 `#` 开头
4. **数据准确性**: 数据来自官方 API，实时更新
5. **网络访问**: 国内可能需要代理才能访问 API

## 📧 联系方式

如有问题，请提交 Issue 或联系开发者。

---

**Made with ❤️ for Clash Royale Community**
