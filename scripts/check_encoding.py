#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查系统编码设置
"""

import os
import sys
import locale

def check_encoding():
    """检查系统编码设置"""
    print("=" * 50)
    print("系统编码检查工具")
    print("=" * 50)
    
    # 获取系统信息
    print("\n系统信息:")
    print(f"操作系统: {os.name} - {sys.platform}")
    print(f"Python版本: {sys.version}")
    
    # 检查默认编码
    print("\n编码设置:")
    print(f"默认编码: {sys.getdefaultencoding()}")
    print(f"文件系统编码: {sys.getfilesystemencoding()}")
    print(f"本地语言设置: {locale.getpreferredencoding()}")
    
    # 检查环境变量
    print("\n相关环境变量:")
    print(f"PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING', '未设置')}")
    print(f"LANG: {os.environ.get('LANG', '未设置')}")
    print(f"LC_ALL: {os.environ.get('LC_ALL', '未设置')}")
    print(f"PYTHONLEGACYWINDOWSSTDIO: {os.environ.get('PYTHONLEGACYWINDOWSSTDIO', '未设置')}")
    
    # 检查潜在问题
    print("\n潜在问题分析:")
    
    # 对于Windows系统
    if os.name == 'nt':
        if locale.getpreferredencoding() != 'utf-8' and locale.getpreferredencoding() != 'UTF-8':
            print("⚠️ Windows系统默认使用非UTF-8编码，可能导致字符显示问题")
            print("  解决方案: 在命令提示符或PowerShell中运行 'chcp 65001' 切换到UTF-8编码")
        
        if 'PYTHONIOENCODING' not in os.environ:
            print("⚠️ PYTHONIOENCODING环境变量未设置，可能导致输出字符问题")
            print("  解决方案: 设置环境变量 PYTHONIOENCODING=utf-8")
    
    # 对于类Unix系统
    else:
        if not (os.environ.get('LANG', '').endswith('.UTF-8') or 
                os.environ.get('LC_ALL', '').endswith('.UTF-8')):
            print("⚠️ LANG或LC_ALL环境变量未设置为UTF-8，可能导致字符问题")
            print("  解决方案: 设置环境变量 LANG=en_US.UTF-8 或适合您地区的UTF-8设置")
    
    # 提供解决方案
    print("\n推荐解决方案:")
    print("1. 在运行程序前设置环境变量:")
    if os.name == 'nt':  # Windows
        print("   - 设置临时环境变量: ")
        print("     set PYTHONIOENCODING=utf-8")
        print("     set PYTHONLEGACYWINDOWSSTDIO=1")
        print("   - 或在PowerShell中: ")
        print("     $env:PYTHONIOENCODING = 'utf-8'")
        print("     $env:PYTHONLEGACYWINDOWSSTDIO = '1'")
        print("\n2. 在Python脚本开始时添加:")
        print("   import sys")
        print("   sys.stdout.reconfigure(encoding='utf-8')")
        print("   sys.stderr.reconfigure(encoding='utf-8')")
    else:  # Linux/Mac
        print("   export LANG=en_US.UTF-8")
        print("   export LC_ALL=en_US.UTF-8")
        print("   export PYTHONIOENCODING=utf-8")
    
    print("\n3. 在代码中处理文件时始终指定编码:")
    print("   with open('文件名', 'w', encoding='utf-8') as f:")
    print("       f.write('内容')")
    
    print("\n4. 对于Windows cmd/PowerShell控制台:")
    print("   - 命令提示符: chcp 65001")
    print("   - PowerShell: [Console]::OutputEncoding = [System.Text.Encoding]::UTF8")
    
    print("\n祝您编码愉快! 😊")

if __name__ == "__main__":
    check_encoding()
