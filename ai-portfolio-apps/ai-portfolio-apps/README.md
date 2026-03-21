# 🤖 AI Portfolio Apps

> **3 production-ready AI agents** built with Claude API + Streamlit  
> Inspired by [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) (96k ⭐)

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)](https://streamlit.io)
[![Claude](https://img.shields.io/badge/Claude-Sonnet_4-orange?logo=anthropic)](https://anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🚀 Apps

### 1. 🤝 [AI Consultant Agent](./consultant_agent/)
**Describe your business problem → Get a McKinsey-style consulting analysis**
- Root cause analysis using MECE framework
- Prioritized strategic recommendations  
- 90-day action plan with quick wins
- Risk assessment & success metrics

**Live Demo:** [consultant-agent.streamlit.app](https://your-app.streamlit.app)

---

### 2. 📊 [AI VC Due Diligence Agent](./vc_diligence/)
**Enter any startup → Get an investor-grade due diligence report**
- Market sizing (TAM/SAM/SOM)
- Competitive moat analysis with score
- Risk assessment (Top 5 risks)
- Investment verdict with reasoning

**Live Demo:** [vc-diligence.streamlit.app](https://your-app.streamlit.app)

---

### 3. 🚀 [AI Product Launch Planner](./product_launch/)
**Describe your product idea → Get a complete GTM launch plan**
- ICP & positioning statement
- Channel strategy by budget
- Week-by-week launch timeline
- KPIs & 90-day north star metric

**Live Demo:** [product-launch.streamlit.app](https://your-app.streamlit.app)

---

## ⚡ Quick Start (Run Locally)

### Step 1: Clone the repo
```bash
git clone https://github.com/yourusername/ai-portfolio-apps.git
cd ai-portfolio-apps
```

### Step 2: Install dependencies
```bash
pip install -r consultant_agent/requirements.txt
```

### Step 3: Get your API key
Get a free API key from [console.anthropic.com](https://console.anthropic.com)

### Step 4: Run any app
```bash
# AI Consultant Agent
streamlit run consultant_agent/app.py

# VC Due Diligence
streamlit run vc_diligence/app.py

# Product Launch Planner
streamlit run product_launch/app.py
```

Then open `http://localhost:8501` in your browser.

---

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → connect your GitHub repo
4. Set `Main file path` to `consultant_agent/app.py`
5. Click **Deploy** — live in 2 minutes! 🎉

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Anthropic Claude](https://anthropic.com) | AI engine (claude-sonnet-4) |
| [Streamlit](https://streamlit.io) | Web UI — no frontend code needed |
| Python | Backend logic |

---

## 📁 Project Structure

```
ai-portfolio-apps/
├── consultant_agent/
│   ├── app.py              # AI Consultant Agent
│   ├── requirements.txt
│   └── .streamlit/config.toml
├── vc_diligence/
│   ├── app.py              # VC Due Diligence Agent
│   ├── requirements.txt
│   └── .streamlit/config.toml
├── product_launch/
│   ├── app.py              # Product Launch Planner
│   ├── requirements.txt
│   └── .streamlit/config.toml
└── README.md
```

---

## 🙏 Credits

Inspired by [Shubham Saboo's awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)

---

*Built with ❤️ using Claude AI*
