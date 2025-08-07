@echo off
echo 🚀 启动Streamlit SQL生成工具...
cd /d "%~dp0"
python -m streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
pause
