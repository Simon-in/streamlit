#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目安装脚本
"""

import subprocess
import sys
import os
import shutil
from setuptools import setup, find_packages


def install_requirements():
    """安装项目依赖"""
    try:
        print("安装项目依赖...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装完成！")
    except subprocess.CalledProcessError as e:
        print(f"安装依赖失败: {e}")
        sys.exit(1)


def create_starter_script():
    """创建启动脚本"""
    print("创建启动脚本...")
    
    # 为Windows创建bat文件
    with open("start.bat", "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("chcp 65001\n")  # 设置控制台为UTF-8编码
        f.write("echo 正在启动SQL生成器...\n")
        f.write("streamlit run app.py\n")
    
    # 为Linux/Mac创建sh文件
    with open("start.sh", "w", encoding="utf-8") as f:
        f.write("#!/bin/bash\n")
        f.write("echo \"正在启动SQL生成器...\"\n")
        f.write("streamlit run app.py\n")
    
    # 设置start.sh为可执行
    try:
        if os.name != 'nt':  # 如果不是Windows
            subprocess.check_call(["chmod", "+x", "start.sh"])
    except Exception as e:
        print(f"无法设置start.sh为可执行: {e}")
    
    print("启动脚本创建完成!")


def check_project_structure():
    """检查项目结构"""
    print("\n检查项目结构...")
    
    required_dirs = [
        "sql_generator",
        "sql_generator/core",
        "sql_generator/ui",
        "sql_generator/templates",
        "sql_generator/utils",
        "sql_generator/config",
        "sql_generator/assets",
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
            
    if missing_dirs:
        print(f"警告: 缺少以下目录: {', '.join(missing_dirs)}")
        create = input("是否创建这些目录? (y/n): ").lower().strip()
        if create == 'y':
            for directory in missing_dirs:
                os.makedirs(directory, exist_ok=True)
                print(f"已创建目录: {directory}")
            
            # 创建__init__.py文件
            for directory in required_dirs:
                init_file = os.path.join(directory, "__init__.py")
                if not os.path.exists(init_file):
                    with open(init_file, "w", encoding="utf-8") as f:
                        f.write("# -*- coding: utf-8 -*-\n")
                    print(f"已创建文件: {init_file}")
    else:
        print("项目结构检查通过！")


def setup_project():
    """设置项目"""
    print("="*50)
    print("SQL生成工具 - 快速设置")
    print("="*50)
    
    # 检查项目结构
    check_project_structure()
    
    # 安装依赖
    install_requirements()
    
    # 创建启动脚本
    create_starter_script()
    
    print("\n"+"="*50)
    print("设置完成! 使用以下命令启动应用:")
    print("streamlit run app.py")
    print("或者双击 start.bat (Windows) / ./start.sh (Linux/Mac)")
    print("="*50)


def run_setup():
    """运行setuptools安装"""
    setup(
        name="sql_generator",
        version="1.0.0",
        description="SQL语句生成工具",
        author="SQL Generator Team",
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            "streamlit>=1.39.0",
            "pandas>=1.0.0",
            "numpy>=1.18.0",
            "xlrd>=2.0.0",
            "openpyxl>=3.0.0",
            "sqlparse>=0.4.0",
        ],
        entry_points={
            "console_scripts": [
                "sql_generator=sql_generator.ui.main_app:run_app",
            ],
        },
        python_requires='>=3.8',
        zip_safe=False,
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        run_setup()
    else:
        setup_project()
