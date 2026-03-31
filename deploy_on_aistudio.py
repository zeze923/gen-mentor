import subprocess
import sys
import os

def install_dependencies():
    print("正在安装项目依赖，请稍候...")
    # 使用国内镜像源加速安装
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt", 
            "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
        ])
        print("所有依赖安装成功！")
    except Exception as e:
        print(f"依赖安装失败: {e}")

if __name__ == "__main__":
    # 1. 先安装依赖
    install_dependencies()
    
    # 2. 启动 Streamlit 应用
    # 注意：这里我们调用 streamlit 的命令行工具来运行您的前端入口
    import streamlit.web.cli as stcli
    
    # 设置运行参数：运行 frontend/main.py
    sys.argv = [
        "streamlit", 
        "run", 
        "frontend/main.py", 
        "--server.port", "8501", 
        "--server.address", "0.0.0.0"
    ]
    
    print("正在启动 GenMentor 前端界面...")
    sys.exit(stcli.main())
