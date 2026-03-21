import streamlit as st
import requests
import json
from llm_helper import stream_llm, FALLBACK_MODELS

st.set_page_config(page_title="AI VC Due Diligence", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: #F5F7FA; color: #0f172a; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1300px !important; }
[data-testid="stSidebar"] { background: #0f172a !important; }
[data-testid="stSidebar"] * { color: #e8e8f0 !important; }
[data-testid="stSidebar"] .stTextInput input { background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.12) !important; color: #e8e8f0 !important; border-radius: 10px !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 10px !important; }
[data-testid="stSidebar"] label { color: rgba(255,255,255,0.45) !important; font-size: 0.68rem !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
[data-testid="stSidebar"] a { color: #60a5fa !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; }
.page-tag { display: inline-flex; align-items: center; gap: 6px; background: #0f172a; color: #60a5fa; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 1.5px; text-transform: uppercase; padding: 5px 14px; border-radius: 100px; margin-bottom: 16px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 800; color: #0f172a; line-height: 1.15; margin-bottom: 10px; letter-spacing: -0.5px; }
.page-title span { color: #2563eb; }
.page-sub { font-size: 0.98rem; color: #64748b; font-weight: 400; line-height: 1.6; margin-bottom: 32px; }
.divider { border: none; border-top: 1px solid #e2e8f0; margin: 0 0 28px; }
.sec-label { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; letter-spacing: 2px; text-transform: uppercase; color: #94a3b8; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }
.sec-label::after { content: ''; flex: 1; height: 1px; background: #e2e8f0; }
.stTextArea textarea { background: white !important; border: 1.5px solid #e2e8f0 !important; border-radius: 12px !important; color: #0f172a !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; line-height: 1.75 !important; padding: 14px 16px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
.stTextArea textarea:focus { border-color: #2563eb !important; box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important; }
.stTextArea textarea::placeholder { color: #c5c0ba !important; }
.stSelectbox > div > div { background: white !important; border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important; color: #0f172a !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.88rem !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
.stTextInput input { background: white !important; border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important; color: #0f172a !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.88rem !important; }
label { font-size: 0.78rem !important; font-weight: 600 !important; color: #374151 !important; letter-spacing: 0.2px !important; }
.stButton > button { background: #0f172a !important; color: white !important; border: none !important; border-radius: 12px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.92rem !important; font-weight: 600 !important; padding: 14px 28px !important; width: 100% !important; box-shadow: 0 4px 16px rgba(15,23,42,0.22) !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #1e293b !important; transform: translateY(-1px) !important; }
.output-empty { background: white; border: 1.5px dashed #cbd5e1; border-radius: 16px; padding: 52px 36px; text-align: center; }
.output-empty .icon { font-size: 2.8rem; margin-bottom: 14px; }
.output-empty h3 { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #64748b; font-weight: 700; margin-bottom: 8px; }
.output-empty p { font-size: 0.85rem; color: #94a3b8; line-height: 1.7; margin-bottom: 18px; }
.output-tag { display: inline-block; background: #eff6ff; color: #2563eb; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; padding: 4px 11px; border-radius: 6px; margin: 3px; }
.output-card { background: white; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 32px 36px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.92rem; line-height: 1.85; color: #374151; box-shadow: 0 4px 24px rgba(0,0,0,0.06); }
.stDownloadButton > button { background: white !important; color: #374151 !important; border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 500 !important; width: 100% !important; margin-top: 14px !important; box-shadow: none !important; }
.stDownloadButton > button:hover { border-color: #2563eb !important; color: #2563eb !important; }
.page-footer { margin-top: 48px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #c5c0ba; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:28px 20px 20px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:16px;">
        <div style="font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;color:white;margin-bottom:5px;">📊 VC Due Diligence</div>
        <div style="font-size:0.72rem;color:rgba(255,255,255,0.38);line-height:1.6;">Investor-grade startup analysis<br>powered by free LLMs</div>
        <div style="background:rgba(37,99,235,0.18);border:1px solid rgba(37,99,235,0.28);color:#60a5fa;font-family:'JetBrains Mono',monospace;font-size:0.6rem;padding:3px 10px;border-radius:100px;margin-top:12px;display:inline-block;letter-spacing:0.5px;">✦ 100% FREE</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<div style="font-size:0.72rem;color:rgba(255,255,255,0.38);line-height:1.7;padding:0 4px 12px;">Get free API key at <a href="https://openrouter.ai" target="_blank">openrouter.ai</a><br>Sign up → API Keys → Create Key</div>""", unsafe_allow_html=True)
    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-v1-...")
    model = st.selectbox("Model", [
        "google/gemma-3-27b-it:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "deepseek/deepseek-v3-base:free",
        "mistralai/mistral-7b-instruct:free",
        "qwen/qwen3-8b:free",
    ])
    st.divider()
    st.markdown("""<div style="font-size:0.7rem;color:rgba(255,255,255,0.28);line-height:1.8;padding:0 4px;">Free tier limits<br>20 requests / minute<br>200 requests / day</div>""", unsafe_allow_html=True)

st.markdown('<div class="page-tag">✦ Investor-Grade · Free · No credit card</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">AI VC Due <span>Diligence</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Enter any startup — get a complete investor-grade due diligence report instantly.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="sec-label">Startup Details</div>', unsafe_allow_html=True)
    startup_name = st.text_input("Startup Name", placeholder="e.g. Zepto, Linear, Razorpay...")
    pitch = st.text_area("One-liner Pitch", placeholder="e.g. B2B SaaS that automates accounts payable using AI — reduces invoice processing time by 80% for mid-market companies", height=90)
    c1, c2 = st.columns(2)
    with c1:
        stage = st.selectbox("Stage", ["Pre-seed","Seed","Series A","Series B","Series C+"])
        geography = st.selectbox("Market", ["India","USA","SEA","Europe","Global"])
    with c2:
        sector = st.selectbox("Sector", ["SaaS / B2B","Fintech","Healthtech","Edtech","Consumer","AI / ML","D2C","Deeptech","Logistics","Other"])
        revenue = st.selectbox("Revenue", ["Pre-revenue","<$100K ARR","$100K–$1M","$1M–$10M","$10M+"])
    extra = st.text_area("Extra Context (optional)", placeholder="Team background, traction, investors, key metrics...", height=70)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    submit = st.button("Run Due Diligence Report →")

with col2:
    st.markdown('<div class="sec-label">DD Report</div>', unsafe_allow_html=True)

    if submit:
        if not api_key:
            st.error("⚠️ Add your OpenRouter API key in the sidebar — free at openrouter.ai")
        elif not startup_name or not pitch:
            st.error("⚠️ Fill in startup name and pitch.")
        else:
            prompt = f"""You are a General Partner at a top-tier VC firm (Sequoia / Accel caliber).

Startup: {startup_name}
Pitch: {pitch}
Stage: {stage} | Sector: {sector} | Market: {geography} | Revenue: {revenue}
Context: {extra or 'Not provided'}

Write a complete investor due diligence report:

## 🎯 Investment Thesis
Why this could be a fund-returner (2–3 sentences).

## 🌊 Market Analysis
- TAM / SAM / SOM with rough estimates
- Why now? Key tailwinds
- Market timing score: [X/10]

## ⚔️ Competitive Landscape
- Top 3 competitors with 1-line description
- Differentiation / moat
- Defensibility score: [X/10]

## 💰 Business Model
- Revenue model clarity
- Unit economics (LTV/CAC)
- Scalability: High/Medium/Low

## 🚨 Top 5 Risks
| Risk | Severity | Mitigation |

## 🔑 Key DD Questions for Founders
5 pointed questions a VC would ask.

## ✅ Investment Verdict
- Decision: PASS / WATCHLIST / INVEST
- Why: 2–3 sentence reasoning
- If invest: valuation range + conditions

Be direct. Think skeptical-but-open VC."""

            try:
                out = st.empty()
                with st.spinner("Generating... (auto-switching model if rate limited)"):
                    full, used_model = stream_llm(api_key, model, prompt, out)
                st.caption(f"✓ Generated with `{used_model}`")
                st.download_button("⬇ Download DD Report (.md)", data=full, file_name=f"{startup_name.lower().replace(' ','_')}_dd.md", mime="text/markdown")
            except Exception as e:
                st.error(f"⚠️ {str(e)}")
    else:
        st.markdown("""
        <div class="output-empty">
            <div class="icon">📊</div>
            <h3>Ready to analyze</h3>
            <p>Enter any startup on the left<br>and click Run Due Diligence.</p>
            <div>
                <span class="output-tag">Market Sizing</span>
                <span class="output-tag">Moat Score</span>
                <span class="output-tag">Risk Assessment</span>
                <span class="output-tag">DD Questions</span>
                <span class="output-tag">Verdict</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="page-footer">Built with Llama 3.3 · OpenRouter · Streamlit &nbsp;·&nbsp; Inspired by awesome-llm-apps (96k ⭐) &nbsp;·&nbsp; github.com/yourusername/ai-portfolio-apps</div>', unsafe_allow_html=True)
