@echo off
REM 设置控制台为UTF-8编码
chcp 65001 > nul

REM 设置环境变量
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=1

REM 启动应用
echo 正在启动SQL生成器...
python app.py

REM 如果出现错误，暂停以便查看错误消息
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 启动过程中发生错误，错误代码: %ERRORLEVEL%
    echo 请运行 python scripts\check_encoding.py 检查编码设置
    pause
)
