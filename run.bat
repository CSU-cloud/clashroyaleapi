@echo off
chcp 65001 >nul
title Clash Royale API 工具集

echo ============================================================
echo   Clash Royale API 工具集 - 一键启动脚本
echo ============================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python！
    echo.
    echo 请先安装 Python: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo [✓] Python 已安装
echo.

REM 检查是否安装了 requests
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装依赖 requests...
    pip install requests
    if errorlevel 1 (
        echo [错误] 安装失败！请手动运行: pip install requests
        pause
        exit /b 1
    )
    echo [✓] 依赖安装完成
    echo.
)

echo [✓] 依赖已就绪
echo.

REM 检查是否设置了 API Key
if "%CLASH_ROYALE_API_KEY%"=="" (
    echo ============================================================
    echo   未检测到 API Key！
    echo ============================================================
    echo.
    echo 请选择配置方式:
    echo.
    echo [1] 手动输入 API Key（临时使用）
    echo [2] 编辑脚本文件（永久配置）
    echo [3] 前往获取 API Key
    echo [4] 退出
    echo.
    set /p choice=请输入选项 (1-4):

    if "%choice%"=="1" goto input_key
    if "%choice%"=="2" goto edit_script
    if "%choice%"=="3" goto get_api_key
    if "%choice%"=="4" exit
    goto invalid_choice

    :input_key
    echo.
    set /p API_KEY=请输入你的 API Key:
    if "%API_KEY%"=="" (
        echo [错误] API Key 不能为空！
        pause
        exit /b 1
    )
    set CLASH_ROYALE_API_KEY=%API_KEY%
    echo.
    echo [✓] API Key 已设置（仅本次有效）
    echo.
    goto run_script

    :edit_script
    echo.
    echo [提示] 正在打开 clashroyaleapi.py...
    echo 请找到第 567 行附近的:
    echo   config.api_key = "YOUR_API_KEY_HERE"
    echo 将其改为你的 API Key
    echo.
    notepad clashroyaleapi.py
    echo 修改完成后，请重新运行此脚本
    pause
    exit /b 0

    :get_api_key
    echo.
    echo [提示] 正在打开 Clash Royale 开发者网站...
    start https://developer.clashroyale.com/
    echo.
    echo 请按照以下步骤获取 API Key:
    echo 1. 登录 Supercell ID
    echo 2. 点击 "My Account"
    echo 3. 点击 "Create New Key"
    echo 4. 填写信息（IP 地址可搜索 "我的IP"）
    echo 5. 复制生成的 Key
    echo.
    echo 获取后请重新运行此脚本
    pause
    exit /b 0

    :invalid_choice
    echo.
    echo [错误] 无效选项！
    pause
    exit /b 1
)

echo [✓] API Key 已配置
echo.

:run_script
echo ============================================================
echo   正在启动 Clash Royale API 工具集...
echo ============================================================
echo.

python clashroyaleapi.py

echo.
echo ============================================================
echo   程序运行完成
echo ============================================================
echo.
pause
