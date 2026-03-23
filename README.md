# 知行智航 · 智能学习导航系统

> 本项目基于 [GenMentor](https://github.com/GeminiLight/gen-mentor) 开源框架进行二次开发与深度定制。GenMentor 是由香港科技大学（广州）与微软研究院联合提出的多智能体智能辅导系统，发表于 WWW 2025。本项目在其原有框架基础上，针对国内教育场景进行了本地化适配与功能扩展，并将底层大模型全面替换为 **DeepSeek**。

---

## 项目简介

本系统是一个由大语言模型驱动的目标导向智能学习平台。系统以学习者的具体职业目标为起点，自动识别能力差距，规划个性化学习路径，并生成定制化学习内容，实现从"目标设定"到"目标达成"的完整学习闭环。

---

## 核心功能模块

- 🧭 **技能差距识别**：分析学习者当前能力，精准映射目标所需技能，识别能力缺口
- 👤 **动态学习者建模**：从认知状态、学习偏好、行为模式三个维度构建并实时更新个人画像
- 🗓️ **个性化路径规划**：基于画像与技能差距，生成逻辑递进、动态可调的学习路径
- 📝 **定制内容生成**：通过"探索—起草—整合"机制，生成适配学习者水平的学习文档与测验
- 🤖 **AI对话辅导**：通过对话方式实时解答学习者疑问，提供学习支持

---

## 技术说明

本项目使用 **DeepSeek** 作为核心大语言模型，驱动上述所有智能体模块的推理与生成任务。DeepSeek 在中文语境下具备出色的语义理解能力，适合国内教育场景的高频调用需求。

---

## 快速开始

1.所需环境
- 使用python 3.11
- 已有git
- 有anaconda
如果本来就有python 3.11，那么就可以不使用conda来创建环境，直接使用python自带的venv的虚拟环境应该也可以（我没试过，可以去ai一下，如果用了python自带的venv的虚拟环境以下激活环境的命令不再适用）
2.把github项目导入pycharm
- 点击欢迎界面上的 "Get from VCS" (或者如果已经打开了项目，点菜单栏 Git -> Clone...)。
- 在弹出的窗口中：
  - URL: 粘贴 GitHub 的项目地址。(具体地址：https://github.com/zeze923/gen-mentor.git)
  - Directory (目录): 点击文件夹图标，选择 D盘 或 E盘 的位置。可以在那里新建一个文件夹。
- 点击 Clone。
- PyCharm 会自动下载所有文件，并且按正确的结构展示
3.配置虚拟环境
这个项目需要 两个独立的虚拟环境：
1. 后端环境：在 backend 文件夹里。
2. 前端环境：在 frontend 文件夹里。
(1) 后端(backend)环境
- 打开终端，在项目genmentor\backend（不一定是genmentor,而是看具体的文件名）下，先创建环境
conda create -n genmentor_backend python=3.11 -y
- 激活环境
conda activate genmentor_backend
- 安装uv
pip install uv
- 安装uv上面的不行的话，使用conda安装（前面如果成功请跳过）
conda install -c conda-forge uv
- 安装依赖
uv pip install -r requirements.txt
(2) 前端(frontend)环境
- 退出后端环境并切换目录 
conda deactivate
cd ..\frontend
- 创建conda环境
conda create -n genmentor_frontend python=3.11 -y
- 激活环境
conda activate genmentor_frontend
- 安装uv
pip install uv
- 安装依赖
uv pip install -r requirements.txt
4.启动项目
(1) 启动后端backend
- 确保现在的终端是在后端环境：
  路径：E:\project\backend (按照实际路径判断)
  环境：(genmentor_backend)
- 激活后端环境：
conda activate genmentor_backend
- 配置deepseek key
  把backend下面的.env.example文件重命名成.env
  把内容修改成如下
    DEEPSEEK_API_KEY="sk-3a5d15d60bfd49df8760d38ad38487d6"
    DEEPSEEK_API_BASE="https://api.deepseek.com/v1"
- 在终端中启动命令 
set HF_ENDPOINT=https://hf-mirror.com
uvicorn main:app --reload --port 5000
 成功标志：会看到绿色的字 Uvicorn running on http://127.0.0.1:5000，并且没有报错。(请保持这个窗口不要关闭！) 
(2) 启动前端(frontend)
- 打开一个新的终端窗口(在 PyCharm 里点 + 号)。
- 切换到前端目录：
cd frontend
- 激活前端环境： 
conda activate genmentor_frontend
- 启动命令
set NO_PROXY=localhost,127.0.0.1(请求本地直连)
streamlit run main.py --server.port 8501
 成功标志：浏览器应该会自动弹 GenMentor 的网页界面( http://0.0.0.0:8501 ),但是这个项目在浏览器里面是无法打开的，我们需要把这个网址改成http://127.0.0.1:8501 
