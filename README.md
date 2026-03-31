<div align="center">
  <p align="center">
    <img src="resources/logo.png" alt="GenMentor Logo" width="300"/>
  </p>
  <p><b>LLM-powered & Goal-oriented Tutoring System</b></p>

  <p>
    <a href="https://www.tianfuwang.tech/gen-mentor">Website</a> &nbsp;·&nbsp;
    <a href="https://arxiv.org/pdf/2501.15749">Paper</a> &nbsp;·&nbsp;
    <a href="https://gen-mentor.streamlit.app/">Demo</a> &nbsp;·&nbsp;
    <a href="https://youtu.be/vTdtGZop-Zc">Video</a>
  </p>

</div>

---

> [!IMPORTANT]  
> :sparkles: Welcome to visit the [GenMentor website](https://www.tianfuwang.tech/gen-mentor) to learn more about our work!

This is official code of our paper "*LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System*", accepted by **WWW 2025 (Industry Track) as an Oral Presentation**.

In this paper, we propose GenMentor, a large language model (LLM)-powered multi-agent framework designed for goal-oriented learning in Intelligent Tutoring Systems (ITS). This framework emphasizes personalization, adaptive learning, and goal-aligned content delivery, making it a robust solution for professional and lifelong learning scenarios.

## 🇨🇳 快速开始（本地演示 + 自建 SearXNG）

以下是简体中文的快速上手说明，包含本地 SearXNG 搜索与前后端启动：

1) 使用 Docker 启动本地 SearXNG

```powershell
docker pull ghcr.io/searxng/searxng:latest
docker run -d --name searxng -p 8080:8080 ^
  -e SEARXNG_SECRET=localdevsecret ^
  -e BASE_URL=http://localhost:8080/ ^
  -v "E:\github\searxng-config:/etc/searxng" ghcr.io/searxng/searxng:latest
```

2) 配置后端使用 SearXNG（已默认）

编辑 `backend/config/default.yaml`（本仓库已默认）：

```yaml
search:
  provider: searx
  base_url: http://127.0.0.1:8080
  max_results: 4
  loader_type: web
  timeout: 8
  load_page_content: false
  loader_timeout: 8
  loader_concurrency: 4
```

3) 安装依赖并启动后端

```powershell
pip install -r backend/requirements.txt
# 如需加速 HuggingFace 下载（当前会话生效）
$env:HF_ENDPOINT="https://hf-mirror.com"
$env:HUGGINGFACE_HUB_CACHE="E:\hf-cache"
$env:HF_HUB_ENABLE_HF_TRANSFER="1"
python backend\main.py
```

4) 启动前端

```powershell
cd frontend
streamlit run main.py --server.port 18501
```

5) 前端启用“使用搜索”后发起请求，即可通过本地 SearXNG 联网。

说明：
- 关闭正文抓取可显著提速；需要更丰富内容时再开启 `search.load_page_content: true`
- 若首次下载嵌入模型较慢，请按上面的镜像环境变量配置


## 🏫 ITS Paradigm Comparison

<div align="center">
  <p align="center">
    <img src="resources/its-paradigms.png" alt="GenMentor Overview" width="500" style="box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-radius: 8px;"/>
  </p>
</div>

| Paradigm | Typical characteristics | Primary focus |
|---|---|---|
| 🏫 Traditional MOOC | Static syllabus; pre-recorded lectures; fragmented learning | Broad access, low personalization |
| 🤖 Chatbot ITS | Reactive Q&A; rule/LLM-driven; session-based help | Instant support, limited long-term adaptation |
| 🎯 Goal-oriented ITS | Proactive planning; personalized paths; goal-aligned assessments | Targeted skill acquisition, continual adaptation |




**🤖 Key Agent Modules**

<div align="center">
  <p align="center">
    <img src="resources/genmentor-framework.png" alt="GenMentor Overview" width="700" style="box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-radius: 8px;"/>
  </p>
</div>

- 🧭 `Skill Gap Identifier`: Analyzes learner's current knowledge to identify gaps.
- 👤 `Adaptive Learner Modeler`: Builds and updates learner profiles based on interactions.
- 🗓️ `Learning Path Scheduler`: Creates personalized learning paths and schedules.
- 📝 `Tailored Content Generator`: Produces customized learning materials and assessments.
- 🧑‍🏫 `AI Chatbot Tutor`: Engages learners in dialogue, answering questions and providing support.

**Key Demo Interfaces**

<div align="center">
  <p align="center">
    <img src="resources/genmentor_demo_1.png" alt="GenMentor Demo Interface-1" width="400" style="box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-radius: 8px; margin: 8px;"/>
    <img src="resources/genmentor_demo_2.png" alt="GenMentor Demo Interface-2" width="400" style="box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-radius: 8px; margin: 8px;"/>
    <img src="resources/genmentor_demo_3.png" alt="GenMentor Demo Interface-3" width="400" style="box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-radius: 8px; margin: 8px;"/>
    <img src="resources/genmentor_demo_4.png" alt="GenMentor Demo Interface-4" width="400" style="box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-radius: 8px; margin: 8px;"/>
    <img src="resources/genmentor_demo_5.png" alt="GenMentor Demo Interface-5" width="400" style="box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-radius: 8px; margin: 8px;"/>
  </p>
</div>

## 🚀 Quick start

Here, we briefly describe how to set up and run the GenMentor system locally. Please see more details in the respective `backend/` and `frontend/` directories.

### 🛠️ Installation

1. Backend environment setup

```bash
cd backend
uv venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

2. Frontend environment setup

```bash
cd frontend
uv venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### ⚙️ Configuration

1. Configure LLM secrets (at least one) for backend

*Option A*: update a `.env` file in `backend/`

```plaintext
# Example for OpenAI:
OPENAI_API_KEY="your-openai-api-key"

# Example for DeepSeek:
DEEPSEEK_API_KEY="your-deepseek-api-key"
```

*Option B*: export environment variables in your shell

```bash
# Example for OpenAI:
export OPENAI_API_KEY="your-openai-api-key"

# Example for DeepSeek:
export DEEPSEEK_API_KEY="your-deepseek-api-key"
DEEPSEEK_API_KEY="your-deepseek-api-key"
```

2. Configure api endpoint for frontend

If you would like to run the backend on a different host/port, please update the API URL in `frontend/config.py`:

```python
backend_endpoint = "http://127.0.0.1:5000/"
```

### ▶️ Running Locally

> [!NOTE]
> The default ports are 5000 for backend, 8501 for frontend by default

*Option A*: Manual (preferred when using separate venvs)

```bash
# start backend
cd backend
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
uvicorn main:app --reload --port 5000
```

```bash
# start frontend
cd frontend
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
streamlit run main.py --server.port 8501
```

*Option B*: Helper scripts (single shell; assumes uvicorn/streamlit on PATH)

```bash
# start backend
bash ./scripts/start_backend.sh [PORT]

# start frontend
bash ./scripts/start_frontend.sh [PORT]

# stop all
bash ./scripts/stop_all.sh
```

### 🌐 Accessing the App

Finally, you can access:

- Backend API: http://127.0.0.1:5000/
- Frontend UI: http://127.0.0.1:8501/

## 🚀 Demo Version of Web Application

Welcome to explore the demo version of the GenMentor web application:

[GenMentor Web App](https://gen-mentor.streamlit.app/)

This interactive demo showcases GenMentor's core functionalities, including:

- Skill Gap Identification: Precisely map learner goals to required skills.
- Adaptive Learner Modeling: Capture learner progress and preferences.
- Personalized Content Delivery: Generate tailored learning resources.

You could also watch the demo video for a quick overview (click the image below):

[![Video Preview](https://img.youtube.com/vi/vTdtGZop-Zc/0.jpg)](https://youtu.be/vTdtGZop-Zc)

## 📚 Citation

```bibtex
@inproceedings{wang2025llm,
  title={LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System},
  author={Wang, Tianfu and Zhan, Yi and Lian, Jianxun and Hu, Zhengyu and Yuan, Nicholas Jing and Zhang, Qi and Xie, Xing and Xiong, Hui},
  booktitle={Companion Proceedings of the ACM Web Conference},
  year={2025}
}
```
