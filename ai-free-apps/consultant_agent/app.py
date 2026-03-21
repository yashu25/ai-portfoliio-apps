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

def call_llm(api_key, model, prompt, placeholder):
    models_to_try = [model] + [m for m in MODELS if m != model]
    for m in models_to_try:
        full = ""
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": m, "messages": [{"role": "user", "content": prompt}], "stream": True, "max_tokens": 1800},
                stream=True, timeout=60
            )
            if r.status_code == 429 or r.status_code == 404:
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
                        except: pass
            placeholder.markdown(f'<div class="out">{full}</div>', unsafe_allow_html=True)
            return full, m
        except Exception as e:
            if "429" in str(e) or "404" in str(e): continue
            raise e
    raise Exception("Saare models rate-limited hain. 2 minute baad retry karo.")

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
.stButton > button { background: #1a1a2e !important; color: white !important; border: none !important; border-radius: 12px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.92rem !important; font-weight: 600 !important; padding: 14px 28px !important; width: 100% !important; box-shadow: 0 4px 16px rgba(26,26,46,0.22) !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #2d2d50 !important; transform: translateY(-1px) !important; }
.out { background: white; border: 1.5px solid #e2ddd5; border-radius: 16px; padding: 32px 36px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.92rem; line-height: 1.85; color: #374151; box-shadow: 0 4px 24px rgba(0,0,0,0.07); }
.empty-box { background: white; border: 1.5px dashed #ddd8d0; border-radius: 16px; padding: 52px 36px; text-align: center; }
.empty-box .icon { font-size: 2.8rem; margin-bottom: 14px; }
.empty-box h3 { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #6b6b80; font-weight: 700; margin-bottom: 8px; }
.empty-box p { font-size: 0.85rem; color: #9ca3af; line-height: 1.7; margin-bottom: 18px; }
.tag { display: inline-block; background: #f3f0ff; color: #7c3aed; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; padding: 4px 11px; border-radius: 6px; margin: 3px; }
.stDownloadButton > button { background: white !important; color: #374151 !important; border: 1.5px solid #e2ddd5 !important; border-radius: 10px !important; font-size: 0.82rem !important; width: 100% !important; margin-top: 14px !important; box-shadow: none !important; }
.stDownloadButton > button:hover { border-color: #7c3aed !important; color: #7c3aed !important; }
.footer { margin-top: 48px; padding-top: 20px; border-top: 1px solid #e2ddd5; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #c5c0ba; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:28px 20px 20px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:16px;">
        <div style="font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;color:white;margin-bottom:5px;">🤝 AI Consultant</div>
        <div style="font-size:0.72rem;color:rgba(255,255,255,0.38);line-height:1.6;">McKinsey-style analysis<br>powered by free LLMs</div>
        <div style="background:rgba(124,58,237,0.18);border:1px solid rgba(124,58,237,0.28);color:#a78bfa;font-family:'JetBrains Mono',monospace;font-size:0.6rem;padding:3px 10px;border-radius:100px;margin-top:12px;display:inline-block;">✦ 100% FREE</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<div style="font-size:0.72rem;color:rgba(255,255,255,0.38);line-height:1.7;padding:0 4px 12px;">
    Free key → <a href="https://openrouter.ai" target="_blank">openrouter.ai</a><br>
    Sign up → API Keys → Create
    </div>""", unsafe_allow_html=True)
    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-v1-...")
    model = st.selectbox("Model (auto-fallback on error)", MODELS)
    st.divider()
    st.markdown("""<div style="font-size:0.7rem;color:rgba(255,255,255,0.28);line-height:1.8;padding:0 4px;">
    Free · 20 req/min · 200 req/day<br>Auto-switches if one fails
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="page-tag">✦ AI-Powered · Free · No credit card</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">AI Consultant <span>Agent</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Describe your business problem — get a McKinsey-style analysis instantly.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="sec-label">Your Problem</div>', unsafe_allow_html=True)
    industry = st.selectbox("Industry", ["Technology / SaaS","E-Commerce / Retail","Healthcare","Finance / Fintech","Education","Manufacturing","Consulting / Services","Startup","Other"])
    company_size = st.selectbox("Company Size", ["Startup (1–10)","Small (11–50)","Mid-size (51–500)","Enterprise (500+)"])
    problem = st.text_area("Business Problem", placeholder="e.g. Our SaaS has 30% monthly churn. Freemium conversion is only 3%. Competitors undercutting pricing. What to do?", height=220)
    framework = st.selectbox("Framework", ["Auto — AI picks best fit","MECE + Issue Tree","McKinsey 7S","Jobs To Be Done","Porter's 5 Forces","SWOT + Strategic Options"])
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    submit = st.button("Analyze with AI Consultant →")

with col2:
    st.markdown('<div class="sec-label">Consulting Analysis</div>', unsafe_allow_html=True)
    if submit:
        if not api_key:
            st.error("⚠️ Add OpenRouter API key in sidebar — free at openrouter.ai")
        elif not problem.strip():
            st.error("⚠️ Please describe your business problem.")
        else:
            fw = "" if "Auto" in framework else f"Use the {framework} framework."
            prompt = f"""You are a senior McKinsey partner with 15 years experience.

Client: {industry} | {company_size}
Problem: {problem}
{fw}

## 🎯 Problem Statement
One crisp sentence.

## 🔍 Root Cause Analysis
3–4 MECE root causes.

## 💡 Top 3 Recommendations
Each: What | Why | Impact | Effort (H/M/L)

## 📅 90-Day Plan
- Weeks 1–2: Quick wins
- Month 1: Foundation  
- Months 2–3: Scale

## ⚠️ Top 3 Risks + Mitigations

## 📈 Success Metrics (4–5 KPIs)

Be specific. No fluff."""

            try:
                out = st.empty()
                with st.spinner("Analyzing... auto-switching model if one fails"):
                    full, used = call_llm(api_key, model, prompt, out)
                st.caption(f"✓ Generated with `{used}`")
                st.download_button("⬇ Download (.md)", data=full, file_name="consulting_analysis.md", mime="text/markdown")
            except Exception as e:
                st.error(f"⚠️ {str(e)}")
    else:
        st.markdown("""
        <div class="empty-box">
            <div class="icon">📋</div>
            <h3>Ready to analyze</h3>
            <p>Fill in your problem on the left<br>and click Analyze.</p>
            <div>
                <span class="tag">Root Causes</span>
                <span class="tag">Recommendations</span>
                <span class="tag">90-Day Plan</span>
                <span class="tag">Risk Assessment</span>
                <span class="tag">KPIs</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="footer">Built with OpenRouter · Streamlit · Inspired by awesome-llm-apps (96k ⭐)</div>', unsafe_allow_html=True)
