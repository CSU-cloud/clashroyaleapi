#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash Royale API 使用示例
功能：查询部落、玩家、卡牌等信息
"""

from clashroyale import Client


def main():
    # ==================== 配置区域 ====================
    # 请在这里填入你的 API Key（从 https://developer.clashroyale.com/ 获取）
    API_KEY = "YOUR_API_KEY_HERE"

    # 示例标签（你可以改成自己的部落/玩家标签）
    CLAN_TAG = "#2PP"  # 部落标签示例
    PLAYER_TAG = "#2PP"  # 玩家标签示例

    # =================================================

    # 初始化客户端
    try:
        client = Client(API_KEY)
        print("=" * 50)
        print("Clash Royale API 客户端已初始化")
        print("=" * 50)
    except Exception as e:
        print(f"初始化失败: {e}")
        print("请确保你已正确安装 clashroyale 库并填入有效的 API Key")
        return

    # ==================== 部落功能 ====================
    print("\n" + "=" * 50)
    print("🏰 部落信息查询")
    print("=" * 50)

    try:
        # 获取部落基本信息
        clan = client.get_clan(CLAN_TAG)
        print(f"\n部落名称: {clan.name}")
        print(f"部落标签: {clan.tag}")
        print(f"部落等级: {clan.level}")
        print(f"部落分数: {clan.score}")
        print(f"部落类型: {clan.type}")
        print(f"成员数量: {clan.members}/50")
        print(f"所需奖杯: {clan.required_trophies}")
    except Exception as e:
        print(f"获取部落信息失败: {e}")

    try:
        # 获取部落成员列表
        members = client.list_clan_member(CLAN_TAG)
        print(f"\n👥 部落成员 ({len(members)} 人):")
        print("-" * 50)
        for i, member in enumerate(members[:10], 1):  # 只显示前10个成员
            print(f"{i}. {member.name} - 角色: {member.role}, 奖杯: {member.trophies}")
        if len(members) > 10:
            print(f"... 还有 {len(members) - 10} 名成员")
    except Exception as e:
        print(f"获取部落成员失败: {e}")

    try:
        # 获取部落战争日志
        war_log = client.list_clan_war_log(CLAN_TAG)
        print(f"\n⚔️  部落战争日志 (最近 {len(war_log)} 场):")
        print("-" * 50)
        for i, war in enumerate(war_log[:5], 1):  # 只显示最近5场
            print(f"{i}. 结果: {war.result} - 参与者: {war.participants}")
    except Exception as e:
        print(f"获取战争日志失败: {e}")

    try:
        # 获取当前部落战争
        current_war = client.get_clan_current_war(CLAN_TAG)
        print(f"\n🔥 当前部落战争:")
        print("-" * 50)
        print(f"状态: {current_war.state}")
        if hasattr(current_war, 'clan') and current_war.clan:
            print(f"我方部落: {current_war.clan.tag} - 参战人数: {len(current_war.clan.participants)}")
    except Exception as e:
        print(f"获取当前战争失败: {e}")

    # ==================== 玩家功能 ====================
    print("\n" + "=" * 50)
    print("👤 玩家信息查询")
    print("=" * 50)

    try:
        # 获取玩家基本信息
        player = client.get_player(PLAYER_TAG)
        print(f"\n玩家名称: {player.name}")
        print(f"玩家标签: {player.tag}")
        print(f"经验等级: {player.exp_level}")
        print(f"奖杯数: {player.trophies}")
        print(f"最高奖杯: {player.best_trophies}")
        print(f"胜利次数: {player.wins}")
        print(f"失败次数: {player.losses}")
        print(f"部落: {player.clan.name if player.clan else '无'}")
    except Exception as e:
        print(f"获取玩家信息失败: {e}")

    try:
        # 获取玩家即将获得的宝箱
        chests = client.get_player_upcoming_chest(PLAYER_TAG)
        print(f"\n📦 即将获得的宝箱 (未来 {len(chests)} 个):")
        print("-" * 50)
        for chest in chests[:10]:  # 只显示前10个
            print(f"第 {chest.index} 个: {chest.name}")
    except Exception as e:
        print(f"获取宝箱信息失败: {e}")

    try:
        # 获取玩家战斗日志
        battles = client.get_player_battle_log(PLAYER_TAG)
        print(f"\n📜 最近战斗记录 (最近 {len(battles)} 场):")
        print("-" * 50)
        for i, battle in enumerate(battles[:5], 1):  # 只显示最近5场
            print(f"{i}. 类型: {battle.type} - 结果: {battle.result}")
    except Exception as e:
        print(f"获取战斗日志失败: {e}")

    # ==================== 卡牌功能 ====================
    print("\n" + "=" * 50)
    print("🃏 卡牌信息")
    print("=" * 50)

    try:
        # 获取所有卡牌
        cards = client.list_card()
        print(f"\n游戏中共有 {len(cards)} 张卡牌:")
        print("-" * 50)
        for i, card in enumerate(cards[:20], 1):  # 只显示前20张
            print(f"{i}. {card.name} - 稀有度: {card.rarity}")
        if len(cards) > 20:
            print(f"... 还有 {len(cards) - 20} 张卡牌")
    except Exception as e:
        print(f"获取卡牌列表失败: {e}")

    print("\n" + "=" * 50)
    print("✅ 查询完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
