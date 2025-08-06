#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pip镜像源配置脚本 - 设置清华大学镜像源
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def get_pip_config_dir():
    """获取pip配置目录"""
    system = platform.system().lower()
    
    if system == "windows":
        # Windows: %APPDATA%\pip\
        config_dir = Path(os.environ.get("APPDATA", "")) / "pip"
    else:
        # Linux/macOS: ~/.config/pip/ 或 ~/.pip/
        config_dir = Path.home() / ".config" / "pip"
        if not config_dir.exists():
            config_dir = Path.home() / ".pip"
    
    return config_dir


def create_pip_config():
    """创建pip配置文件"""
    config_dir = get_pip_config_dir()
    config_file = config_dir / "pip.conf"
    
    # 创建配置目录
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # pip配置内容
    config_content = """[global]
# 清华大学镜像源
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/

# 信任清华镜像源
trusted-host = pypi.tuna.tsinghua.edu.cn

# 备用镜像源（如果主镜像源不可用）
extra-index-url = https://mirrors.aliyun.com/pypi/simple/
                  https://pypi.douban.com/simple/

[install]
# 安装时的默认选项
trusted-host = pypi.tuna.tsinghua.edu.cn
               mirrors.aliyun.com
               pypi.douban.com
"""
    
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(config_content)
        
        print(f"✅ pip配置文件已创建: {config_file}")
        return True
        
    except Exception as e:
        print(f"❌ 创建pip配置文件失败: {e}")
        return False


def test_mirror_speed():
    """测试镜像源速度"""
    mirrors = {
        "清华大学": "https://pypi.tuna.tsinghua.edu.cn/simple/",
        "阿里云": "https://mirrors.aliyun.com/pypi/simple/",
        "豆瓣": "https://pypi.douban.com/simple/",
        "官方源": "https://pypi.org/simple/"
    }
    
    print("\n🚀 测试镜像源连接速度...")
    print("-" * 50)
    
    for name, url in mirrors.items():
        try:
            # 使用pip命令测试连接
            cmd = [sys.executable, "-m", "pip", "search", "--index-url", url, "pip", "--timeout", "10"]
            start_time = __import__("time").time()
            
            # 由于pip search已被禁用，改用简单的HTTP请求测试
            import urllib.request
            import urllib.error
            
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'pip/21.0.1')
            
            with urllib.request.urlopen(request, timeout=10) as response:
                end_time = __import__("time").time()
                response_time = round((end_time - start_time) * 1000, 2)
                
                if response_time < 1000:
                    status = "🟢 极快"
                elif response_time < 3000:
                    status = "🟡 较快"
                else:
                    status = "🔴 较慢"
                
                print(f"{name:<8}: {response_time:>8}ms {status}")
                
        except Exception as e:
            print(f"{name:<8}: {'超时':>8}    🔴 无法连接")
    
    print("-" * 50)


def configure_pip_mirror():
    """配置pip镜像源"""
    print("🔧 Pip镜像源配置工具")
    print("=" * 50)
    
    # 检查当前配置
    print("\n📋 检查当前pip配置...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "config", "list"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            if result.stdout.strip():
                print("当前pip配置:")
                print(result.stdout)
            else:
                print("当前没有pip配置")
        else:
            print("无法获取pip配置")
    except Exception as e:
        print(f"检查pip配置时出错: {e}")
    
    # 测试镜像源速度
    test_mirror_speed()
    
    # 询问用户是否要配置
    print("\n❓ 是否要配置清华镜像源？")
    print("1. 是 - 创建配置文件")
    print("2. 是 - 使用pip config命令")
    print("3. 否 - 退出")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == "1":
        # 方法1：创建配置文件
        print("\n📝 创建pip配置文件...")
        if create_pip_config():
            print("✅ 配置完成！")
            print("\n🔍 验证配置...")
            verify_configuration()
        
    elif choice == "2":
        # 方法2：使用pip config命令
        print("\n⚙️  使用pip config命令配置...")
        configure_with_command()
        
    elif choice == "3":
        print("\n👋 退出配置")
        return
    
    else:
        print("\n❌ 无效选择，退出配置")
        return


def configure_with_command():
    """使用pip config命令配置"""
    commands = [
        [sys.executable, "-m", "pip", "config", "set", "global.index-url", "https://pypi.tuna.tsinghua.edu.cn/simple/"],
        [sys.executable, "-m", "pip", "config", "set", "global.trusted-host", "pypi.tuna.tsinghua.edu.cn"],
    ]
    
    success_count = 0
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {' '.join(cmd[4:])}")
                success_count += 1
            else:
                print(f"❌ {' '.join(cmd[4:])}: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ 执行命令失败: {e}")
    
    if success_count == len(commands):
        print("\n✅ 所有配置已完成！")
        verify_configuration()
    else:
        print(f"\n⚠️  部分配置失败 ({success_count}/{len(commands)})")


def verify_configuration():
    """验证配置是否生效"""
    print("\n🔍 验证配置...")
    
    try:
        # 检查配置
        result = subprocess.run([sys.executable, "-m", "pip", "config", "list"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            config_output = result.stdout.lower()
            if "tsinghua" in config_output:
                print("✅ 清华镜像源配置已生效")
            else:
                print("⚠️  配置可能未生效，请检查")
            
            print("\n当前配置:")
            print(result.stdout)
        else:
            print("❌ 无法验证配置")
    
    except Exception as e:
        print(f"验证配置时出错: {e}")
    
    # 测试安装
    print("\n🧪 测试安装包...")
    test_install()


def test_install():
    """测试包安装"""
    print("尝试安装测试包 'wheel'...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "wheel"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ 测试安装成功！镜像源工作正常")
        else:
            print("❌ 测试安装失败:")
            print(result.stderr)
    except Exception as e:
        print(f"测试安装时出错: {e}")


def show_usage_tips():
    """显示使用提示"""
    print("\n" + "=" * 50)
    print("📖 使用提示")
    print("=" * 50)
    
    print("\n🔧 临时使用镜像源:")
    print("   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ <package>")
    
    print("\n🔧 永久配置镜像源:")
    print("   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/")
    
    print("\n🔧 查看当前配置:")
    print("   pip config list")
    
    print("\n🔧 重置配置:")
    print("   pip config unset global.index-url")
    
    print("\n🌐 其他镜像源:")
    print("   阿里云: https://mirrors.aliyun.com/pypi/simple/")
    print("   豆瓣:   https://pypi.douban.com/simple/")
    print("   腾讯云: https://mirrors.cloud.tencent.com/pypi/simple/")
    
    print("\n📁 配置文件位置:")
    config_dir = get_pip_config_dir()
    print(f"   {config_dir / 'pip.conf'}")


def main():
    """主函数"""
    print("🚀 Pip镜像源配置工具")
    print("帮助您快速配置清华大学pip镜像源，提升包安装速度")
    
    try:
        configure_pip_mirror()
        show_usage_tips()
        
        print("\n" + "=" * 50)
        print("✅ 配置完成！现在您可以享受更快的pip安装速度了！")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 配置过程中出现错误: {e}")
        print("请检查网络连接或手动配置镜像源")


if __name__ == "__main__":
    main() 