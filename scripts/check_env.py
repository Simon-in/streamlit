#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本 - 检查项目运行环境和依赖
"""

import sys
import platform
import subprocess
from pathlib import Path


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"📋 {title}")
    print("=" * 60)


def check_python_environment():
    """检查Python环境"""
    print_header("Python环境检查")
    
    # Python版本
    version = sys.version_info
    print(f"🐍 Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python版本满足要求 (>= 3.8)")
    else:
        print("❌ Python版本过低，需要Python 3.8或更高版本")
        return False
    
    # Python路径
    print(f"📍 Python路径: {sys.executable}")
    
    # 平台信息
    print(f"💻 操作系统: {platform.system()} {platform.release()}")
    print(f"🏗️  架构: {platform.machine()}")
    
    return True


def check_pip():
    """检查pip"""
    print_header("包管理器检查")
    
    try:
        import pip
        print(f"✅ pip已安装: {pip.__version__}")
        
        # 检查pip版本
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"📦 pip版本: {result.stdout.strip()}")
        
        return True
    except ImportError:
        print("❌ pip未安装")
        return False


def check_required_packages():
    """检查必需的包"""
    print_header("核心依赖检查")
    
    required_packages = {
        "streamlit": "Streamlit框架",
        "pandas": "数据处理",
        "numpy": "数值计算",
        "openpyxl": "Excel文件处理",
        "PIL": "图像处理 (Pillow)",
        "altair": "数据可视化"
    }
    
    missing_packages = []
    
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package:<12} - {description}")
        except ImportError:
            print(f"❌ {package:<12} - {description} (未安装)")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages


def check_optional_packages():
    """检查可选包"""
    print_header("可选依赖检查")
    
    optional_packages = {
        "psutil": "性能监控",
        "magic": "文件类型检测",
        "sqlparse": "SQL格式化",
        "typing_extensions": "类型提示扩展"
    }
    
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print(f"✅ {package:<18} - {description}")
        except ImportError:
            print(f"⚠️  {package:<18} - {description} (可选，未安装)")


def check_project_structure():
    """检查项目结构"""
    print_header("项目结构检查")
    
    required_files = [
        "../app.py",
        "../sql_generator/core/sql_generator.py",
        "../sql_generator/core/sql_formatter.py",
        "../sql_generator/core/advanced_sql.py",
        "../sql_generator/ui/main_app.py",
        "../sql_generator/utils/file_utils.py",
        "../sql_generator/utils/security.py",
        "../sql_generator/config/constants.py",
        "../requirements.txt"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (缺失)")
            missing_files.append(file_path)
    
    return len(missing_files) == 0, missing_files


def check_streamlit_config():
    """检查Streamlit配置"""
    print_header("Streamlit配置检查")
    
    try:
        import streamlit as st
        print(f"✅ Streamlit版本: {st.__version__}")
        
        # 检查配置目录
        config_dir = Path.home() / ".streamlit"
        if config_dir.exists():
            print(f"📁 配置目录: {config_dir}")
        else:
            print("📁 配置目录: 不存在 (将使用默认配置)")
        
        return True
    except ImportError:
        print("❌ Streamlit未安装")
        return False


def provide_solutions(missing_packages, missing_files):
    """提供解决方案"""
    print_header("解决方案")
    
    if missing_packages:
        print("📦 缺失包的安装方法:")
        
        print("\n方法1 - 使用清华镜像安装基础依赖:")
        print("   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements-minimal.txt")
        
        print("\n方法2 - 使用清华镜像安装完整依赖:")
        print("   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt")
        
        print("\n方法3 - 单独安装缺失的包:")
        for package in missing_packages:
            if package == "PIL":
                print(f"   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ Pillow")
            else:
                print(f"   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ {package}")
    
    if missing_files:
        print("\n📁 缺失文件:")
        print("   请确保项目文件完整，可能需要重新下载项目")
        for file in missing_files:
            print(f"   - {file}")
    
    print("\n🔧 常见问题解决:")
    print("   1. 使用清华镜像源（推荐）:")
    print("      pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ <package>")
    print("   2. 权限问题: 使用 --user 参数")
    print("      pip install --user <package>")
    print("   3. 版本冲突: 使用虚拟环境")
    print("      python -m venv venv")
    print("      source venv/bin/activate  # Linux/Mac")
    print("      venv\\Scripts\\activate     # Windows")
    print("   4. 永久配置清华镜像源:")
    print("      pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/")


def main():
    """主检查流程"""
    print("🔍 Streamlit SQL生成工具 - 环境检查")
    
    # 检查Python环境
    python_ok = check_python_environment()
    
    # 检查pip
    pip_ok = check_pip()
    
    # 检查项目结构
    structure_ok, missing_files = check_project_structure()
    
    # 检查必需包
    packages_ok, missing_packages = check_required_packages()
    
    # 检查可选包
    check_optional_packages()
    
    # 检查Streamlit
    streamlit_ok = check_streamlit_config()
    
    # 总结
    print_header("检查结果总结")
    
    all_checks = [
        ("Python环境", python_ok),
        ("包管理器", pip_ok), 
        ("项目结构", structure_ok),
        ("核心依赖", packages_ok),
        ("Streamlit配置", streamlit_ok)
    ]
    
    passed = 0
    for check_name, result in all_checks:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name:<12}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 检查通过率: {passed}/{len(all_checks)} ({passed/len(all_checks)*100:.0f}%)")
    
    if passed == len(all_checks):
        print("\n🎉 环境检查全部通过! 可以正常运行项目")
        print("\n🚀 启动命令:")
        print("   streamlit run app.py")
    else:
        print(f"\n⚠️  发现 {len(all_checks)-passed} 个问题，请参考下方解决方案")
        provide_solutions(missing_packages, missing_files)


if __name__ == "__main__":
    main() 