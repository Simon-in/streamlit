#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键配置脚本 - 配置pip镜像源并安装依赖
"""

import sys
import subprocess
import platform


def run_command(command, description=""):
    """执行命令并处理错误"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - 成功")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - 失败")
        print(f"错误信息: {e.stderr}")
        return False, e.stderr


def main():
    """主配置流程"""
    print("🚀 Streamlit SQL生成工具 - 一键配置脚本")
    print("=" * 60)
    
    print("本脚本将为您完成以下操作:")
    print("1. 配置pip清华镜像源")
    print("2. 升级pip到最新版本") 
    print("3. 安装项目依赖")
    print("4. 验证安装结果")
    
    input("\n按回车键继续...")
    
    # 1. 配置pip镜像源
    print("\n" + "=" * 40)
    print("📦 步骤 1: 配置pip镜像源")
    print("=" * 40)
    
    mirror_commands = [
        f"{sys.executable} -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/",
        f"{sys.executable} -m pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn"
    ]
    
    for cmd in mirror_commands:
        run_command(cmd, f"配置镜像源")
    
    # 2. 升级pip
    print("\n" + "=" * 40)
    print("⬆️  步骤 2: 升级pip")
    print("=" * 40)
    
    run_command(f"{sys.executable} -m pip install --upgrade pip", "升级pip")
    
    # 3. 安装依赖
    print("\n" + "=" * 40)
    print("📥 步骤 3: 安装项目依赖")
    print("=" * 40)
    
    print("选择安装模式:")
    print("1. 基础安装 (仅核心功能)")
    print("2. 完整安装 (包含所有功能)")
    
    choice = input("\n请选择 (1/2) [默认: 1]: ").strip() or "1"
    
    if choice == "1":
        requirements_file = "requirements-minimal.txt"
        print("📦 安装基础依赖...")
    else:
        requirements_file = "requirements.txt"
        print("📦 安装完整依赖...")
    
    success, output = run_command(
        f"{sys.executable} -m pip install -r {requirements_file}",
        f"安装依赖包"
    )
    
    if not success:
        print("\n⚠️  如果安装失败，请尝试:")
        print("1. 检查网络连接")
        print("2. 使用管理员权限运行")
        print("3. 手动安装: pip install -r requirements-minimal.txt")
        return False
    
    # 4. 验证安装
    print("\n" + "=" * 40)
    print("🔍 步骤 4: 验证安装")
    print("=" * 40)
    
    # 检查核心包
    core_packages = ["streamlit", "pandas", "numpy", "openpyxl", "PIL"]
    failed_packages = []
    
    for package in core_packages:
        try:
            __import__(package)
            print(f"✅ {package} - 已安装")
        except ImportError:
            print(f"❌ {package} - 未安装")
            failed_packages.append(package)
    
    # 5. 创建启动脚本
    print("\n" + "=" * 40)
    print("📝 步骤 5: 创建启动脚本")
    print("=" * 40)
    
    # Windows批处理文件
    if platform.system() == "Windows":
        startup_script = """@echo off
echo 🚀 启动Streamlit SQL生成工具...
cd /d "%~dp0"
python -m streamlit run main/main.py --server.enableCORS false --server.enableXsrfProtection false
pause
"""
        try:
            with open("start.bat", "w", encoding="utf-8") as f:
                f.write(startup_script)
            print("✅ 已创建 start.bat 启动脚本")
        except Exception as e:
            print(f"❌ 创建启动脚本失败: {e}")
    
    # Unix/Linux shell脚本
    startup_script_sh = """#!/bin/bash
echo "🚀 启动Streamlit SQL生成工具..."
cd "$(dirname "$0")"
python3 -m streamlit run main/main.py --server.enableCORS false --server.enableXsrfProtection false
"""
    try:
        with open("start.sh", "w", encoding="utf-8") as f:
            f.write(startup_script_sh)
        
        # 添加执行权限
        if platform.system() != "Windows":
            import os
            os.chmod("start.sh", 0o755)
        
        print("✅ 已创建 start.sh 启动脚本")
    except Exception as e:
        print(f"❌ 创建启动脚本失败: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    if len(failed_packages) == 0:
        print("🎉 配置完成！所有依赖都已成功安装")
        print("=" * 60)
        
        print("\n🚀 启动应用:")
        if platform.system() == "Windows":
            print("   方式1: 双击 start.bat 文件")
        print("   方式2: 运行 ./start.sh")
        print("   方式3: 运行 streamlit run main/main.py")
        
        print("\n🌐 应用地址: http://localhost:8501")
        print("📖 详细文档: 查看 README.md")
        
        # 询问是否立即启动
        start_now = input("\n是否现在启动应用？(y/N): ").strip().lower()
        if start_now in ['y', 'yes']:
            print("\n🚀 启动应用...")
            try:
                subprocess.run([sys.executable, "-m", "streamlit", "run", "main/main.py", 
                              "--server.enableCORS", "false", 
                              "--server.enableXsrfProtection", "false"])
            except KeyboardInterrupt:
                print("\n👋 应用已停止")
            except Exception as e:
                print(f"\n❌ 启动失败: {e}")
    else:
        print("⚠️  配置完成，但有部分依赖安装失败")
        print("=" * 60)
        print(f"失败的包: {', '.join(failed_packages)}")
        print("\n💡 建议:")
        print("1. 检查网络连接")
        print("2. 尝试手动安装失败的包")
        print("3. 运行 python check_env.py 进行环境诊断")
    
    return len(failed_packages) == 0


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ 一键配置成功完成！")
        else:
            print("\n⚠️  配置过程中出现问题，请查看上述信息")
    except KeyboardInterrupt:
        print("\n\n👋 用户取消配置")
    except Exception as e:
        print(f"\n❌ 配置过程中出现错误: {e}")
        sys.exit(1) 