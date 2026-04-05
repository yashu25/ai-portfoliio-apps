import streamlit as st
import requests
import json

MODELS = [
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "qwen/qwen3-8b:free",
    "microsoft/phi-3-mini-128k-instruct:free",
]

# ---------------- FRAMEWORK LOGIC ---------------- #
def get_framework_prompt(framework):

    if "Auto" in framework:
        return "", "3–4 root causes."

    if "MECE" in framework:
        return """
Use strict MECE Issue Tree logic.
Break problem into mutually exclusive, collectively exhaustive buckets.
""", "3–4 MECE root causes."

    if "McKinsey 7S" in framework:
        return """
Use McKinsey 7S Framework:
Strategy, Structure, Systems, Shared Values, Skills, Style, Staff
""", "Analyze across 7S elements."

    if "Jobs To Be Done" in framework:
        return """
Use Jobs To Be Done framework.

Break into:
- Functional Jobs
- Emotional Jobs
- Social Jobs

Identify:
- Hiring triggers
- Pain points
- Desired outcomes
""", "Analyze using JTBD (Functional, Emotional, Social Jobs)."

    if "Porter" in framework:
        return """
Use Porter’s 5 Forces:
- Rivalry
- Supplier Power
- Buyer Power
- Substitutes
- New Entrants
""", "Analyze using Porter’s 5 Forces."

    if "SWOT" in framework:
        return """
Use SWOT:
Strengths, Weaknesses, Opportunities, Threats
""", "Analyze using SWOT."

    return "", "3–4 root causes."

# ---------------- LLM CALL ---------------- #
def call_llm(api_key, model, prompt, placeholder):
    models_to_try = [model] + [m for m in MODELS if m != model]
    for m in models_to_try:
        full = ""
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key.strip()}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": m,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                    "max_tokens": 1800
                },
                stream=True,
                timeout=60
            )

            if r.status_code in [429, 404]:
                continue

            if r.status_code != 200:
                raise Exception(f"API Error {r.status_code}: {r.text}")

            for line in r.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: ") and line != "data: [DONE]":
                        try:
                            delta = json.loads(line[6:])["choices"][0]["delta"].get("content", "")
                            if delta:
                                full += delta
                                placeholder.markdown(f'<div class="out">{full}▌</div>', unsafe_allow_html=True)
                        except:
                            pass

            placeholder.markdown(f'<div class="out">{full}</div>', unsafe_allow_html=True)
            return full, m

        except Exception as e:
            if "429" in str(e) or "404" in str(e):
                continue
            raise e

    raise Exception("Saare models rate-limited hain. 2 minute baad retry karo.")

# ---------------- UI ---------------- #

st.set_page_config(page_title="AI Consultant Agent", page_icon="🤝", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: #F7F5F0; color: #1a1a2e; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1300px !important; }
[data-testid="stSidebar"] { background: #1a1a2e !important; }
[data-testid="stSidebar"] * { color: #e8e8f0 !important; }
[data-testid="stSidebar"] .stTextInput input { background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.15) !important; color: #e8e8f0 !important; border-radius: 10px !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 10px !important; }
[data-testid="stSidebar"] label { color: rgba(255,255,255,0.45) !important; font-size: 0.68rem !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
[data-testid="stSidebar"] a { color: #a78bfa !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; }
.page-tag { display: inline-flex; align-items: center; gap: 6px; background: #1a1a2e; color: #a78bfa; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 1.5px; text-transform: uppercase; padding: 5px 14px; border-radius: 100px; margin-bottom: 16px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 800; color: #1a1a2e; line-height: 1.15; margin-bottom: 10px; }
.page-title span { color: #7c3aed; }
.page-sub { font-size: 0.98rem; color: #6b6b80; line-height: 1.6; margin-bottom: 32px; }
.divider { border: none; border-top: 1px solid #e2ddd5; margin: 0 0 28px; }
.sec-label { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; letter-spacing: 2px; text-transform: uppercase; color: #9ca3af; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }
.sec-label::after { content: ''; flex: 1; height: 1px; background: #e2ddd5; }
.stTextArea textarea { background: white !important; border: 1.5px solid #e2ddd5 !important; border-radius: 12px !important; color: #1a1a2e !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; line-height: 1.75 !important; padding: 14px 16px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important; }
.stTextArea textarea:focus { border-color: #7c3aed !important; box-shadow: 0 0 0 3px rgba(124,58,237,0.08) !important; }
.stTextArea textarea::placeholder { color: #c5c0ba !important; }
.stSelectbox > div > div { background: white !important; border: 1.5px solid #e2ddd5 !important; border-radius: 10px !important; color: #1a1a2e !important; font-size: 0.88rem !important; }
label { font-size: 0.78rem !important; font-weight: 600 !important; color: #374151 !important; }
.stButton > button { background: #1a1a2e !important; color: white !important; border: none !important; border-radius: 12px !important; font-size: 0.92rem !important; font-weight: 600 !important; padding: 14px 28px !important; width: 100% !important; box-shadow: 0 4px 16px rgba(26,26,46,0.22) !important; }
.out { background: white; border: 1.5px solid #e2ddd5; border-radius: 16px; padding: 32px 36px; font-size: 0.92rem; line-height: 1.85; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🤝 AI Consultant")
    api_key = st.text_input("OpenRouter API Key", type="password")
    model = st.selectbox("Model", MODELS)

st.markdown('<div class="page-title">AI Consultant <span>Agent</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    industry = st.selectbox("Industry", ["Technology / SaaS","E-Commerce / Retail","Healthcare","Finance","Education","Startup","Other"])
    company_size = st.selectbox("Company Size", ["Startup","Small","Mid-size","Enterprise"])
    problem = st.text_area("Business Problem")
    framework = st.selectbox("Framework", [
        "Auto — AI picks best fit",
        "MECE + Issue Tree",
        "McKinsey 7S",
        "Jobs To Be Done",
        "Porter's 5 Forces",
        "SWOT + Strategic Options"
    ])
    submit = st.button("Analyze")

with col2:
    if submit:

        if not api_key or not api_key.startswith("sk-"):
            st.error("Enter valid API key")

        elif not problem.strip():
            st.error("Enter problem")

        else:
            fw_prompt, rca_section = get_framework_prompt(framework)

            prompt = f"""
You are a senior McKinsey consultant.

STRICT:
- Follow selected framework ONLY
- Do NOT default to MECE unless selected

Client: {industry} | {company_size}
Problem: {problem}

{fw_prompt}

## 🎯 Problem Statement
One crisp sentence.

## 🔍 Root Cause Analysis
{rca_section}

## 💡 Recommendations

## 📅 Plan

## ⚠️ Risks

## 📈 KPIs
"""

            try:
                out = st.empty()
                with st.spinner("Analyzing..."):
                    full, used = call_llm(api_key, model, prompt, out)

                st.success(f"Generated using {used}")

            except Exception as e:
                st.error(str(e))
