import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Product Launch Planner", page_icon="🚀", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: #F5FBF7; color: #0f2318; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1300px !important; }
[data-testid="stSidebar"] { background: #0f2318 !important; }
[data-testid="stSidebar"] * { color: #e8f0ea !important; }
[data-testid="stSidebar"] .stTextInput input { background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.12) !important; color: #e8f0ea !important; border-radius: 10px !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 10px !important; }
[data-testid="stSidebar"] label { color: rgba(255,255,255,0.45) !important; font-size: 0.68rem !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
[data-testid="stSidebar"] a { color: #6ee7b7 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; }
.page-tag { display: inline-flex; align-items: center; gap: 6px; background: #0f2318; color: #6ee7b7; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 1.5px; text-transform: uppercase; padding: 5px 14px; border-radius: 100px; margin-bottom: 16px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 800; color: #0f2318; line-height: 1.15; margin-bottom: 10px; letter-spacing: -0.5px; }
.page-title span { color: #059669; }
.page-sub { font-size: 0.98rem; color: #4b7060; font-weight: 400; line-height: 1.6; margin-bottom: 32px; }
.divider { border: none; border-top: 1px solid #d1e8da; margin: 0 0 28px; }
.sec-label { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; letter-spacing: 2px; text-transform: uppercase; color: #7aab90; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }
.sec-label::after { content: ''; flex: 1; height: 1px; background: #d1e8da; }
.stTextArea textarea { background: white !important; border: 1.5px solid #d1e8da !important; border-radius: 12px !important; color: #0f2318 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; line-height: 1.75 !important; padding: 14px 16px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
.stTextArea textarea:focus { border-color: #059669 !important; box-shadow: 0 0 0 3px rgba(5,150,105,0.08) !important; }
.stTextArea textarea::placeholder { color: #b8ccbf !important; }
.stSelectbox > div > div { background: white !important; border: 1.5px solid #d1e8da !important; border-radius: 10px !important; color: #0f2318 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.88rem !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
.stTextInput input { background: white !important; border: 1.5px solid #d1e8da !important; border-radius: 10px !important; color: #0f2318 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.88rem !important; }
label { font-size: 0.78rem !important; font-weight: 600 !important; color: #2d4a38 !important; letter-spacing: 0.2px !important; }
.stButton > button { background: #0f2318 !important; color: white !important; border: none !important; border-radius: 12px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.92rem !important; font-weight: 600 !important; padding: 14px 28px !important; width: 100% !important; box-shadow: 0 4px 16px rgba(15,35,24,0.22) !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #1a3d28 !important; transform: translateY(-1px) !important; }
.output-empty { background: white; border: 1.5px dashed #b8d4c0; border-radius: 16px; padding: 52px 36px; text-align: center; }
.output-empty .icon { font-size: 2.8rem; margin-bottom: 14px; }
.output-empty h3 { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #4b7060; font-weight: 700; margin-bottom: 8px; }
.output-empty p { font-size: 0.85rem; color: #7aab90; line-height: 1.7; margin-bottom: 18px; }
.output-tag { display: inline-block; background: #ecfdf5; color: #059669; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; padding: 4px 11px; border-radius: 6px; margin: 3px; }
.output-card { background: white; border: 1.5px solid #d1e8da; border-radius: 16px; padding: 32px 36px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.92rem; line-height: 1.85; color: #374151; box-shadow: 0 4px 24px rgba(0,0,0,0.06); }
.stDownloadButton > button { background: white !important; color: #374151 !important; border: 1.5px solid #d1e8da !important; border-radius: 10px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 500 !important; width: 100% !important; margin-top: 14px !important; box-shadow: none !important; }
.stDownloadButton > button:hover { border-color: #059669 !important; color: #059669 !important; }
.page-footer { margin-top: 48px; padding-top: 20px; border-top: 1px solid #d1e8da; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #a8c4b0; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:28px 20px 20px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:16px;">
        <div style="font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;color:white;margin-bottom:5px;">🚀 Launch Planner</div>
        <div style="font-size:0.72rem;color:rgba(255,255,255,0.38);line-height:1.6;">Full GTM plan generator<br>powered by free LLMs</div>
        <div style="background:rgba(5,150,105,0.18);border:1px solid rgba(5,150,105,0.28);color:#6ee7b7;font-family:'JetBrains Mono',monospace;font-size:0.6rem;padding:3px 10px;border-radius:100px;margin-top:12px;display:inline-block;letter-spacing:0.5px;">✦ 100% FREE</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<div style="font-size:0.72rem;color:rgba(255,255,255,0.38);line-height:1.7;padding:0 4px 12px;">Get free API key at <a href="https://openrouter.ai" target="_blank">openrouter.ai</a><br>Sign up → API Keys → Create Key</div>""", unsafe_allow_html=True)
    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-v1-...")
    model = st.selectbox("Model", [
        "meta-llama/llama-3.3-70b-instruct:free",
        "google/gemma-3-27b-it:free",
        "deepseek/deepseek-v3-base:free",
        "mistralai/mistral-7b-instruct:free",
        "qwen/qwen3-8b:free",
    ])
    st.divider()
    st.markdown("""<div style="font-size:0.7rem;color:rgba(255,255,255,0.28);line-height:1.8;padding:0 4px;">Free tier limits<br>20 requests / minute<br>200 requests / day</div>""", unsafe_allow_html=True)

st.markdown('<div class="page-tag">✦ GTM Strategy · Free · No credit card</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">AI Product <span>Launch Planner</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Describe your product idea — get a complete go-to-market launch plan in seconds.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="sec-label">Product Details</div>', unsafe_allow_html=True)
    product_name = st.text_input("Product Name", placeholder="e.g. FlowDesk, NovaPay, MediScan...")
    product_desc = st.text_area("What does it do?", placeholder="e.g. An AI tool that converts meeting recordings into structured PRDs and JIRA tickets automatically — built for product managers at Series A+ startups", height=110)
    c1, c2 = st.columns(2)
    with c1:
        audience = st.selectbox("Target Audience", ["B2B — Enterprise","B2B — SMBs","B2B — Startups","B2C — Consumers","B2C — Professionals","Developers","Prosumer"])
        timeline = st.selectbox("Launch In", ["ASAP (< 1 month)","1–3 months","3–6 months","6–12 months"])
    with c2:
        budget = st.selectbox("Marketing Budget", ["Bootstrap (< $5K)","Seed ($5K–$50K)","Growth ($50K–$500K)","Scale ($500K+)"])
        category = st.selectbox("Category", ["Productivity / SaaS","AI Tool","Consumer App","Developer Tool","Marketplace","Fintech","Health","E-Commerce","Other"])
    usp = st.text_area("Your Unique Advantage", placeholder="What makes this 10x better than alternatives?", height=65)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    submit = st.button("Generate GTM Launch Plan →")

with col2:
    st.markdown('<div class="sec-label">GTM Launch Plan</div>', unsafe_allow_html=True)

    if submit:
        if not api_key:
            st.error("⚠️ Add your OpenRouter API key in the sidebar — free at openrouter.ai")
        elif not product_name or not product_desc:
            st.error("⚠️ Fill in product name and description.")
        else:
            prompt = f"""You are a world-class Product Marketing Manager (ex-Stripe, Notion, Linear).

Product: {product_name}
Description: {product_desc}
Target: {audience} | Category: {category}
Timeline: {timeline} | Budget: {budget}
USP: {usp or 'Not specified'}

Build a complete Go-To-Market launch plan:

## 🎯 Positioning Statement
"For [target], {product_name} is the [category] that [key benefit], unlike [alternative]."

## 👥 Ideal Customer Profile (ICP)
- Exact persona (job title, company, pain point)
- Where they discover products like this
- Their buying trigger

## 📣 Top 3 Launch Channels
For each: **Channel** | **Tactic** | **Expected reach** | **Cost**
(Tailored to {budget} budget)

## 📅 Launch Timeline
- **T-4 weeks:** Pre-launch (build waitlist, tease)
- **T-2 weeks:** Soft launch (beta, feedback)
- **Launch Day:** Exact plan
- **T+2 weeks:** Momentum (retargeting, press)

## 💬 Messaging Framework
- Hero headline (under 10 words)
- 3 key messages (one per pain point)
- Primary CTA

## 📊 Launch KPIs
- Week 1 target
- Month 1 target
- 90-day north star metric

## ⚡ 3 Things To Do This Week
Specific, actionable. No vague advice."""

            try:
                out = st.empty()
                full = ""
                with st.spinner(f"Building launch plan for {product_name}..."):
                    with requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "HTTP-Referer": "https://yashconsultsagentically.streamlit.app", "X-Title": "AI Product Launch Planner"},
                        json={"model": model, "messages": [{"role":"user","content":prompt}], "stream": True, "max_tokens": 1800},
                        stream=True
                    ) as r:
                        if r.status_code != 200:
                            st.error(f"API Error {r.status_code}: {r.text}")
                        else:
                            for line in r.iter_lines():
                                if line:
                                    line = line.decode("utf-8")
                                    if line.startswith("data: ") and line != "data: [DONE]":
                                        try:
                                            d = json.loads(line[6:])
                                            delta = d["choices"][0]["delta"].get("content","")
                                            if delta:
                                                full += delta
                                                out.markdown(f'<div class="output-card">{full}▌</div>', unsafe_allow_html=True)
                                        except: pass
                            out.markdown(f'<div class="output-card">{full}</div>', unsafe_allow_html=True)
                st.download_button("⬇ Download Launch Plan (.md)", data=full, file_name=f"{product_name.lower().replace(' ','_')}_launch_plan.md", mime="text/markdown")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
    else:
        st.markdown("""
        <div class="output-empty">
            <div class="icon">🚀</div>
            <h3>Ready to plan</h3>
            <p>Describe your product on the left<br>and click Generate.</p>
            <div>
                <span class="output-tag">Positioning</span>
                <span class="output-tag">ICP</span>
                <span class="output-tag">Channels</span>
                <span class="output-tag">Timeline</span>
                <span class="output-tag">KPIs</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="page-footer">Built with Llama 3.3 · OpenRouter · Streamlit &nbsp;·&nbsp; Inspired by awesome-llm-apps (96k ⭐) &nbsp;·&nbsp; github.com/yourusername/ai-portfolio-apps</div>', unsafe_allow_html=True)
