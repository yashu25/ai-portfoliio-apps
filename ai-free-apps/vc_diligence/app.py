import streamlit as st
import requests
import json

st.set_page_config(page_title="AI VC Due Diligence", page_icon="📊", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #050d1a; color: #e8e8f0; }
.stTextArea textarea { background-color: #0d1a2e; color: #e8e8f0; border: 1px solid #1e3a5f; }
.stTextInput input { background-color: #0d1a2e; color: #e8e8f0; border: 1px solid #1e3a5f; }
.stSelectbox > div > div { background-color: #0d1a2e; }
.output-box { background-color: #0d1a2e; border: 1px solid #3b82f6; border-radius: 10px; padding: 20px; margin-top: 10px; white-space: pre-wrap; font-size: 0.9rem; line-height: 1.7; }
h1 { color: #3b82f6 !important; }
.stButton > button { background: linear-gradient(135deg,#2563eb,#3b82f6); color: white; border: none; border-radius: 8px; font-weight: bold; width: 100%; }
.stButton > button:hover { filter: brightness(1.1); }
.free-badge { background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.3); color: #60a5fa; padding: 4px 12px; border-radius: 100px; font-size: 0.75rem; display: inline-block; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 AI VC Due Diligence Agent")
st.markdown('<span class="free-badge">✓ 100% FREE — Powered by DeepSeek / Llama via OpenRouter</span>', unsafe_allow_html=True)
st.markdown("*Enter any startup → Get an investor-grade due diligence report*")
st.divider()

with st.sidebar:
    st.header("⚙️ Setup")
    st.markdown("""
    **Get free API key:**  
    👉 [openrouter.ai](https://openrouter.ai)  
    Sign up → API Keys tab  
    *(No credit card needed!)*
    """)
    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-v1-...")
    model = st.selectbox("AI Model (all free)", [
        "meta-llama/llama-3.3-70b-instruct:free",
        "deepseek/deepseek-v3-base:free",
        "google/gemma-3-27b-it:free",
        "qwen/qwen3-8b:free",
        "mistralai/mistral-7b-instruct:free",
    ])
    st.divider()
    st.markdown("**Free tier:** 200 req/day  \nNo credit card ever!")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🚀 Startup Info")
    
    startup_name = st.text_input("Startup Name", placeholder="e.g. Zepto, Linear, Razorpay...")
    pitch = st.text_area(
        "One-liner Pitch",
        placeholder="e.g. B2B SaaS that automates accounts payable using AI — reduces invoice processing time by 80% for mid-market companies",
        height=90
    )
    col_a, col_b = st.columns(2)
    with col_a:
        stage = st.selectbox("Stage", ["Pre-seed","Seed","Series A","Series B","Series C+"])
        geography = st.selectbox("Market", ["India","USA","SEA","Europe","Global"])
    with col_b:
        sector = st.selectbox("Sector", [
            "SaaS / B2B","Fintech","Healthtech","Edtech",
            "Consumer","AI / ML","D2C","Deeptech","Logistics","Other"
        ])
        revenue = st.selectbox("Revenue", [
            "Pre-revenue","<$100K ARR","$100K-$1M","$1M-$10M","$10M+"])

    extra = st.text_area("Extra Context (optional)", 
        placeholder="Team background, key metrics, notable investors, competitors...", height=70)
    submit = st.button("🔍 Run Due Diligence Report")

with col2:
    st.subheader("📋 DD Report")

    if submit:
        if not api_key:
            st.error("⚠️ Add your OpenRouter API key (sidebar) — it's free!")
        elif not startup_name or not pitch:
            st.error("⚠️ Fill startup name and pitch")
        else:
            prompt = f"""You are a General Partner at a top-tier VC firm (Sequoia / Accel caliber).
Perform rigorous due diligence on this startup:

Name: {startup_name}
Pitch: {pitch}
Stage: {stage} | Sector: {sector} | Market: {geography} | Revenue: {revenue}
Context: {extra or 'Not provided'}

Write a complete investor due diligence report:

## 🎯 Investment Thesis
Why this could be a fund-returner (2-3 sentences).

## 🌊 Market Analysis
- TAM / SAM / SOM with rough estimates and reasoning
- Why now? Key tailwinds driving this market
- Market timing score: [X/10]

## ⚔️ Competitive Landscape  
- Top 3 direct competitors with 1-line description each
- {startup_name}'s differentiation / moat
- Defensibility score: [X/10] with reasoning

## 💰 Business Model
- Revenue model clarity
- Estimated unit economics (LTV/CAC ratio)
- Scalability: High / Medium / Low with reasoning

## 🚨 Top 5 Risks
| Risk | Severity | Mitigation |
For each risk.

## 🔑 Key DD Questions for Founders
5 pointed questions a VC would ask in the next meeting.

## ✅ Investment Verdict
- **Decision:** PASS / WATCHLIST / INVEST
- **Why:** 2-3 sentence reasoning
- **If invest:** Suggested entry valuation range + key conditions

Be direct. Think skeptical-but-open-minded VC. No vague statements."""

            try:
                output_placeholder = st.empty()
                full_response = ""

                with requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://ai-vc-diligence.streamlit.app",
                        "X-Title": "AI VC Due Diligence Agent"
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": True,
                        "max_tokens": 1800,
                    },
                    stream=True
                ) as response:
                    if response.status_code != 200:
                        st.error(f"API Error: {response.text}")
                    else:
                        for line in response.iter_lines():
                            if line:
                                line = line.decode("utf-8")
                                if line.startswith("data: ") and line != "data: [DONE]":
                                    try:
                                        data = json.loads(line[6:])
                                        delta = data["choices"][0]["delta"].get("content","")
                                        if delta:
                                            full_response += delta
                                            output_placeholder.markdown(
                                                f'<div class="output-box">{full_response}▌</div>',
                                                unsafe_allow_html=True
                                            )
                                    except Exception:
                                        pass

                        output_placeholder.markdown(
                            f'<div class="output-box">{full_response}</div>',
                            unsafe_allow_html=True
                        )
                        st.download_button(
                            "💾 Download DD Report (.md)",
                            data=full_response,
                            file_name=f"{startup_name.lower().replace(' ','_')}_dd_report.md",
                            mime="text/markdown"
                        )
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.markdown("""
        <div class="output-box">
<b>What you'll get:</b>

📈  Market sizing (TAM/SAM/SOM)
⚔️  Competitive moat score
💰  Business model & unit economics
🚨  Top 5 risks with mitigations
🔑  Key DD questions for founders
✅  Investment verdict with reasoning

<b>Try with:</b> Zepto · Razorpay · Notion · Linear
Or analyze <b>your own startup idea!</b>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Free AI · OpenRouter · github.com/yourusername/ai-portfolio-apps")
