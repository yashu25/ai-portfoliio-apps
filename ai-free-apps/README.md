# 🤖 AI Portfolio Apps — 100% Free

> **3 production-ready AI agents** — No credit card, no paid API, totally free  
> Powered by **Llama 3.3 · DeepSeek · Gemma** via OpenRouter

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)](https://streamlit.io)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Free_Models-green)](https://openrouter.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🚀 3 Apps Inside

| App | What it does | Live Demo |
|-----|-------------|-----------|
| 🤝 AI Consultant Agent | Business problem → McKinsey-style analysis | [consultant-agent.streamlit.app](#) |
| 📊 AI VC Due Diligence | Startup → Investor DD report | [vc-diligence.streamlit.app](#) |
| 🚀 AI Product Launch Planner | Product idea → Full GTM plan | [product-launch.streamlit.app](#) |

---

## ⚡ Quick Start

### Step 1: Get free API key (2 minutes)
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up (no credit card needed!)
3. Go to **API Keys** → Create key
4. Copy your key (starts with `sk-or-v1-...`)

### Step 2: Run locally
```bash
git clone https://github.com/yourusername/ai-portfolio-apps.git
cd ai-portfolio-apps
pip install streamlit requests
streamlit run consultant_agent/app.py
```

### Step 3: Deploy free on Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set main file → Deploy!
4. Add `OPENROUTER_API_KEY` in Streamlit secrets (optional)

---

## 🆓 Free Models Used

| Model | Provider | Context | Best for |
|-------|----------|---------|---------|
| `meta-llama/llama-3.3-70b-instruct:free` | Meta | 128K | Best overall quality |
| `deepseek/deepseek-v3-base:free` | DeepSeek | 64K | Analysis & reasoning |
| `google/gemma-3-27b-it:free` | Google | 128K | Structured output |
| `mistralai/mistral-7b-instruct:free` | Mistral | 32K | Fast responses |
| `qwen/qwen3-8b:free` | Alibaba | 32K | Multilingual |

> **Limits:** 20 req/min · 200 req/day — more than enough for demos & resume projects!

---

## 📁 Structure

```
ai-portfolio-apps/
├── consultant_agent/
│   ├── app.py
│   └── requirements.txt
├── vc_diligence/
│   ├── app.py
│   └── requirements.txt
├── product_launch/
│   ├── app.py
│   └── requirements.txt
├── SETUP_GUIDE.md      ← Step by step in Hindi
└── README.md
```

---

## 📝 Resume Line

```
AI Portfolio — 3 Production AI Agents (Free LLM Stack)     2025
• Built 3 AI-powered tools using OpenRouter API (Llama 3.3, DeepSeek, Gemma)
• AI Consultant Agent: McKinsey-style business analysis from natural language input
• VC Due Diligence Agent: Investor-grade startup analysis with risk scoring
• Product Launch Planner: Full GTM plan generator with channel strategy
• Deployed on Streamlit Cloud with real-time streaming responses
• Tech: Python, Streamlit, OpenRouter API (free tier)
• GitHub: github.com/yourusername/ai-portfolio-apps
```

---

*Inspired by [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) (96k ⭐)*
