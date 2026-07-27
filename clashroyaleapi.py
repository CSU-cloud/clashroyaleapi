#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash Royale API 完整工具集
功能：玩家统计、部落分析、卡牌数据、排行榜、数据导出
作者：CSU-cloud
版本：2.0.0
"""

import requests
import json
import csv
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import os


# ==================== 配置管理 ====================
@dataclass
class Config:
    """配置类"""
    api_key: str = "YOUR_API_KEY_HERE"
    base_url: str = "https://api.clashroyale.com/v1"
    timeout: int = 30
    cache_enabled: bool = True
    cache_duration: int = 300  # 5分钟缓存

    def load_from_env(self):
        """从环境变量加载配置"""
        self.api_key = os.getenv("CLASH_ROYALE_API_KEY", self.api_key)
        return self


class ClashRoyaleAPI:
    """Clash Royale API 客户端"""

    def __init__(self, api_key: str = None, config: Config = None):
        """
        初始化 API 客户端

        Args:
            api_key: Clash Royale API 密钥
            config: 配置对象
        """
        if config:
            self.config = config
        else:
            self.config = Config()
            if api_key:
                self.config.api_key = api_key
            else:
                self.config.load_from_env()

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.config.api_key}",
            "Accept": "application/json"
        })

        self._cache = {} if self.config.cache_enabled else None

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        发送 API 请求

        Args:
            endpoint: API 端点
            params: 查询参数

        Returns:
            API 响应数据
        """
        # 检查缓存
        cache_key = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        if self._cache and cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if time.time() - cached_time < self.config.cache_duration:
                return cached_data

        url = f"{self.config.base_url}/{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            data = response.json()

            # 保存到缓存
            if self._cache:
                self._cache[cache_key] = (time.time(), data)

            return data

        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                raise Exception("API 密钥无效或 IP 未授权")
            elif response.status_code == 404:
                raise Exception(f"资源不存在: {endpoint}")
            elif response.status_code == 429:
                raise Exception("API 请求频率超限，请稍后重试")
            else:
                raise Exception(f"API 请求失败: {e}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {e}")

    def _format_tag(self, tag: str) -> str:
        """格式化标签（URL编码）"""
        if tag.startswith("#"):
            tag = tag[1:]
        return tag.upper()

    # ==================== 玩家 API ====================
    def get_player(self, player_tag: str) -> Dict:
        """
        获取玩家信息

        Args:
            player_tag: 玩家标签（如 #2PP）

        Returns:
            玩家信息字典
        """
        tag = self._format_tag(player_tag)
        return self._make_request(f"players/%23{tag}")

    def get_player_upcoming_chests(self, player_tag: str) -> List[Dict]:
        """
        获取玩家即将获得的宝箱

        Args:
            player_tag: 玩家标签

        Returns:
            宝箱列表
        """
        tag = self._format_tag(player_tag)
        data = self._make_request(f"players/%23{tag}/upcomingchests")
        return data.get("items", [])

    def get_player_battle_log(self, player_tag: str, limit: int = 25) -> List[Dict]:
        """
        获取玩家战斗日志

        Args:
            player_tag: 玩家标签
            limit: 返回战斗数量（最大25）

        Returns:
            战斗日志列表
        """
        tag = self._format_tag(player_tag)
        data = self._make_request(f"players/%23{tag}/battlelog")
        return data.get("items", [])[:limit]

    # ==================== 部落 API ====================
    def get_clan(self, clan_tag: str) -> Dict:
        """
        获取部落信息

        Args:
            clan_tag: 部落标签

        Returns:
            部落信息字典
        """
        tag = self._format_tag(clan_tag)
        return self._make_request(f"clans/%23{tag}")

    def list_clan_members(self, clan_tag: str, limit: int = 50) -> List[Dict]:
        """
        获取部落成员列表

        Args:
            clan_tag: 部落标签
            limit: 返回成员数量

        Returns:
            成员列表
        """
        tag = self._format_tag(clan_tag)
        data = self._make_request(f"clans/%23{tag}/members")
        return data.get("items", [])[:limit]

    def get_clan_war_log(self, clan_tag: str, limit: int = 10) -> List[Dict]:
        """
        获取部落战争日志

        Args:
            clan_tag: 部落标签
            limit: 返回战争数量

        Returns:
            战争日志列表
        """
        tag = self._format_tag(clan_tag)
        data = self._make_request(f"clans/%23{tag}/warlog")
        return data.get("items", [])[:limit]

    def get_clan_current_war(self, clan_tag: str) -> Dict:
        """
        获取当前部落战争

        Args:
            clan_tag: 部落标签

        Returns:
            当前战争信息
        """
        tag = self._format_tag(clan_tag)
        return self._make_request(f"clans/%23{tag}/currentwar")

    def search_clans(self, name: str, limit: int = 10) -> List[Dict]:
        """
        搜索部落

        Args:
            name: 部落名称
            limit: 返回数量

        Returns:
            部落列表
        """
        data = self._make_request("clans", params={"name": name, "limit": limit})
        return data.get("items", [])

    # ==================== 卡牌 API ====================
    def list_cards(self) -> List[Dict]:
        """
        获取所有卡牌列表

        Returns:
            卡牌列表
        """
        data = self._make_request("cards")
        return data.get("items", [])

    # ==================== 锦标赛 API ====================
    def search_tournaments(self, name: str, limit: int = 10) -> List[Dict]:
        """
        搜索锦标赛

        Args:
            name: 锦标赛名称
            limit: 返回数量

        Returns:
            锦标赛列表
        """
        data = self._make_request("tournaments", params={"name": name, "limit": limit})
        return data.get("items", [])

    def get_tournament(self, tournament_tag: str) -> Dict:
        """
        获取锦标赛信息

        Args:
            tournament_tag: 锦标赛标签

        Returns:
            锦标赛信息
        """
        tag = self._format_tag(tournament_tag)
        return self._make_request(f"tournaments/%23{tag}")

    # ==================== 排行榜 API ====================
    def get_locations(self) -> List[Dict]:
        """
        获取所有地区列表

        Returns:
            地区列表
        """
        data = self._make_request("locations")
        return data.get("items", [])

    def get_player_rankings(self, location_id: int = 57000019, limit: int = 100) -> List[Dict]:
        """
        获取玩家排行榜

        Args:
            location_id: 地区ID（默认全球）
            limit: 返回数量

        Returns:
            排行榜列表
        """
        data = self._make_request(f"locations/{location_id}/rankings/players",
                                 params={"limit": limit})
        return data.get("items", [])

    def get_clan_rankings(self, location_id: int = 57000019, limit: int = 100) -> List[Dict]:
        """
        获取部落排行榜

        Args:
            location_id: 地区ID（默认全球）
            limit: 返回数量

        Returns:
            排行榜列表
        """
        data = self._make_request(f"locations/{location_id}/rankings/clans",
                                 params={"limit": limit})
        return data.get("items", [])

    # ==================== 数据分析功能 ====================
    def analyze_player_stats(self, player_tag: str) -> Dict:
        """
        分析玩家统计数据

        Args:
            player_tag: 玩家标签

        Returns:
            统计分析结果
        """
        player = self.get_player(player_tag)
        battles = self.get_player_battle_log(player_tag, limit=25)

        # 计算胜率
        wins = sum(1 for b in battles if b.get("result") == "victory")
        total = len(battles)
        win_rate = (wins / total * 100) if total > 0 else 0

        # 计算常用卡牌
        card_usage = {}
        for battle in battles:
            if "team" in battle:
                for card in battle["team"][0].get("cards", []):
                    card_name = card.get("name", "Unknown")
                    card_usage[card_name] = card_usage.get(card_name, 0) + 1

        top_cards = sorted(card_usage.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "player_name": player.get("name"),
            "trophies": player.get("trophies"),
            "best_trophies": player.get("bestTrophies"),
            "level": player.get("expLevel"),
            "wins": player.get("wins"),
            "losses": player.get("losses"),
            "recent_win_rate": f"{win_rate:.1f}%",
            "recent_battles": total,
            "top_cards": [{"name": card[0], "uses": card[1]} for card in top_cards]
        }

    def analyze_clan_stats(self, clan_tag: str) -> Dict:
        """
        分析部落统计数据

        Args:
            clan_tag: 部落标签

        Returns:
            统计分析结果
        """
        clan = self.get_clan(clan_tag)
        members = self.list_clan_members(clan_tag)

        # 计算成员统计
        total_trophies = sum(m.get("trophies", 0) for m in members)
        avg_trophies = total_trophies / len(members) if members else 0

        # 角色分布
        roles = {}
        for member in members:
            role = member.get("role", "member")
            roles[role] = roles.get(role, 0) + 1

        return {
            "clan_name": clan.get("name"),
            "clan_level": clan.get("clanLevel"),
            "members": len(members),
            "total_trophies": total_trophies,
            "avg_trophies": f"{avg_trophies:.0f}",
            "required_trophies": clan.get("requiredTrophies"),
            "role_distribution": roles,
            "top_players": sorted(members, key=lambda x: x.get("trophies", 0), reverse=True)[:5]
        }

    # ==================== 数据导出功能 ====================
    def export_player_to_json(self, player_tag: str, filename: str = None):
        """
        导出玩家数据到 JSON 文件

        Args:
            player_tag: 玩家标签
            filename: 文件名（可选）
        """
        player = self.get_player(player_tag)
        chests = self.get_player_upcoming_chests(player_tag)
        battles = self.get_player_battle_log(player_tag)

        data = {
            "player": player,
            "upcoming_chests": chests,
            "battle_log": battles,
            "export_time": datetime.now().isoformat()
        }

        filename = filename or f"player_{player_tag.replace('#', '')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✓ 玩家数据已导出到: {filename}")

    def export_clan_to_csv(self, clan_tag: str, filename: str = None):
        """
        导出部落成员数据到 CSV 文件

        Args:
            clan_tag: 部落标签
            filename: 文件名（可选）
        """
        members = self.list_clan_members(clan_tag)

        filename = filename or f"clan_{clan_tag.replace('#', '')}_members.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "tag", "name", "role", "expLevel", "trophies",
                "clanRank", "previousClanRank", "donations", "donationsReceived"
            ])
            writer.writeheader()

            for member in members:
                writer.writerow({
                    "tag": member.get("tag"),
                    "name": member.get("name"),
                    "role": member.get("role"),
                    "expLevel": member.get("expLevel"),
                    "trophies": member.get("trophies"),
                    "clanRank": member.get("clanRank"),
                    "previousClanRank": member.get("previousClanRank"),
                    "donations": member.get("donations"),
                    "donationsReceived": member.get("donationsReceived")
                })

        print(f"✓ 部落成员数据已导出到: {filename}")

    def export_cards_to_json(self, filename: str = "cards.json"):
        """
        导出所有卡牌数据到 JSON 文件

        Args:
            filename: 文件名
        """
        cards = self.list_cards()

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)

        print(f"✓ 卡牌数据已导出到: {filename}")


# ==================== 命令行界面 ====================
def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_player_info(client: ClashRoyaleAPI, player_tag: str):
    """打印玩家信息"""
    try:
        player = client.get_player(player_tag)

        print_header(f"玩家信息: {player.get('name')}")
        print(f"标签: {player.get('tag')}")
        print(f"等级: {player.get('expLevel')}")
        print(f"奖杯: {player.get('trophies')}")
        print(f"最高奖杯: {player.get('bestTrophies')}")
        print(f"胜利: {player.get('wins')}")
        print(f"失败: {player.get('losses')}")
        print(f"部落: {player.get('clan', {}).get('name', '无')}")
        print(f"竞技场: {player.get('arena', {}).get('name', '未知')}")

    except Exception as e:
        print(f"✗ 错误: {e}")


def print_clan_info(client: ClashRoyaleAPI, clan_tag: str):
    """打印部落信息"""
    try:
        clan = client.get_clan(clan_tag)

        print_header(f"部落信息: {clan.get('name')}")
        print(f"标签: {clan.get('tag')}")
        print(f"等级: {clan.get('clanLevel')}")
        print(f"分数: {clan.get('clanScore')}")
        print(f"成员: {clan.get('members')}/50")
        print(f"类型: {clan.get('type')}")
        print(f"所需奖杯: {clan.get('requiredTrophies')}")
        print(f"描述: {clan.get('description', '无')[:100]}")

    except Exception as e:
        print(f"✗ 错误: {e}")


def print_analysis(client: ClashRoyaleAPI, player_tag: str):
    """打印玩家统计分析"""
    try:
        stats = client.analyze_player_stats(player_tag)

        print_header(f"玩家统计分析: {stats['player_name']}")
        print(f"当前奖杯: {stats['trophies']}")
        print(f"最高奖杯: {stats['best_trophies']}")
        print(f"等级: {stats['level']}")
        print(f"总胜利: {stats['wins']}")
        print(f"总失败: {stats['losses']}")
        print(f"近期胜率: {stats['recent_win_rate']} (最近{stats['recent_battles']}场)")

        if stats['top_cards']:
            print("\n常用卡牌 (Top 5):")
            for i, card in enumerate(stats['top_cards'], 1):
                print(f"  {i}. {card['name']} - 使用 {card['uses']} 次")

    except Exception as e:
        print(f"✗ 错误: {e}")


def main():
    """主函数 - 演示所有功能"""

    # 初始化客户端
    config = Config()
    config.load_from_env()

    if config.api_key == "YOUR_API_KEY_HERE":
        print("=" * 60)
        print("⚠️  警告: 请先设置 API Key!")
        print("=" * 60)
        print("\n方式 1: 设置环境变量")
        print("  export CLASH_ROYALE_API_KEY='your_key_here'")
        print("\n方式 2: 直接修改代码中的 API_KEY")
        print("\n获取 API Key: https://developer.clashroyale.com/")
        return

    client = ClashRoyaleAPI(config=config)

    print_header("Clash Royale API 完整工具集 v2.0")
    print("功能：玩家查询 | 部落分析 | 排行榜 | 数据导出")

    # 示例标签（请替换为你自己的标签）
    PLAYER_TAG = "#2PP"  # 替换为你的玩家标签
    CLAN_TAG = "#2PP"    # 替换为你的部落标签

    # 1. 查询玩家信息
    print_player_info(client, PLAYER_TAG)

    # 2. 玩家统计分析
    print_analysis(client, PLAYER_TAG)

    # 3. 查询部落信息
    print_clan_info(client, CLAN_TAG)

    # 4. 部落成员分析
    try:
        clan_stats = client.analyze_clan_stats(CLAN_TAG)
        print_header(f"部落统计分析: {clan_stats['clan_name']}")
        print(f"部落等级: {clan_stats['clan_level']}")
        print(f"成员数量: {clan_stats['members']}")
        print(f"总奖杯: {clan_stats['total_trophies']}")
        print(f"平均奖杯: {clan_stats['avg_trophies']}")
        print(f"所需奖杯: {clan_stats['required_trophies']}")

        if clan_stats['top_players']:
            print("\n部落 Top 5 玩家:")
            for i, player in enumerate(clan_stats['top_players'], 1):
                print(f"  {i}. {player.get('name')} - {player.get('trophies')} 奖杯")

    except Exception as e:
        print(f"✗ 错误: {e}")

    # 5. 数据导出示例
    print_header("数据导出")
    try:
        client.export_player_to_json(PLAYER_TAG)
        client.export_clan_to_csv(CLAN_TAG)
        # client.export_cards_to_json()  # 取消注释以导出所有卡牌
        print("\n✓ 数据导出完成!")
    except Exception as e:
        print(f"✗ 导出失败: {e}")

    print_header("✅ 所有查询完成!")


if __name__ == "__main__":
    main()
