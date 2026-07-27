@echo off
chcp 65001 >nul
title Clash Royale API - 快速测试

echo ============================================================
echo   Clash Royale API - 快速测试
echo ============================================================
echo.

REM 创建临时测试文件
echo from clashroyaleapi import ClashRoyaleAPI, Config > temp_test.py
echo. >> temp_test.py
echo config = Config() >> temp_test.py
echo if "%%CLASH_ROYALE_API_KEY%%" != "": >> temp_test.py
echo     config.api_key = "%%CLASH_ROYALE_API_KEY%%" >> temp_test.py
echo. >> temp_test.py
echo if config.api_key == "YOUR_API_KEY_HERE": >> temp_test.py
echo     print("错误: 请先设置 API Key!") >> temp_test.py
echo     print("运行 run.bat 进行配置") >> temp_test.py
echo     exit() >> temp_test.py
echo. >> temp_test.py
echo try: >> temp_test.py
echo     client = ClashRoyaleAPI(config=config) >> temp_test.py
echo     print("测试 1: 获取卡牌列表...") >> temp_test.py
echo     cards = client.list_cards() >> temp_test.py
echo     print(f"✓ 成功! 游戏共有 {len(cards)} 张卡牌") >> temp_test.py
echo     print() >> temp_test.py
echo     print("前 10 张卡牌:") >> temp_test.py
echo     for i, card in enumerate(cards[:10], 1): >> temp_test.py
echo         print(f"  {i}. {card['name']} (稀有度: {card['rarity']})") >> temp_test.py
echo     print() >> temp_test.py
echo     print("=" * 60) >> temp_test.py
echo     print("✓ 所有测试通过! API 连接正常!") >> temp_test.py
echo     print("=" * 60) >> temp_test.py
echo except Exception as e: >> temp_test.py
echo     print(f"✗ 测试失败: {e}") >> temp_test.py

REM 运行测试
python temp_test.py

REM 删除临时文件
del temp_test.py

echo.
pause