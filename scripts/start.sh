#!/bin/bash
echo "🚀 启动Streamlit SQL生成工具..."
cd "$(dirname "$0")"
python3 -m streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
