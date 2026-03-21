import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Product Launch Planner", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #030f0a; color: #e8e8f0; }
.stTextArea textarea { background-color: #071a0f; color: #e8e8f0; border: 1px solid #0d4f2f; }
.stTextInput input { background-color: #071a0f; color: #e8e8f0; border: 1px solid #0d4f2f; }
.stSelectbox > div > div { background-color: #071a0f; }
.output-box { background-color: #071a0f; border: 1px solid #10b981; border-radius: 10px; padding: 20px; margin-top: 10px; white-space: pre-wrap; font-size: 0.9rem; line-height: 1.7; }
h1 { color: #10b981 !important; }
.stButton > button { background: linear-gradient(135deg,#059669,#10b981); color: white; border: none; border-radius: 8px; font-weight: bold; width: 100%; }
.stButton > button:hover { filter: brightness(1.1); }
.free-badge { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); color: #34d399; padding: 4px 12px; border-radius: 100px; font-size: 0.75rem; display: inline-block; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Product Launch Planner")
st.markdown('<span class="free-badge">✓ 100% FREE — Powered by Llama / Gemma via OpenRouter</span>', unsafe_allow_html=True)
st.markdown("*Describe your product → Get a full GTM launch plan in seconds*")
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
        "google/gemma-3-27b-it:free",
        "deepseek/deepseek-v3-base:free",
        "qwen/qwen3-8b:free",
        "mistralai/mistral-7b-instruct:free",
    ])
    st.divider()
    st.markdown("**Free tier:** 200 req/day  \nNo credit card ever!")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📦 Product Details")

    product_name = st.text_input("Product Name", placeholder="e.g. FlowDesk, NovaPay, MediScan...")
    product_desc = st.text_area(
        "What does it do?",
        placeholder="e.g. An AI tool that automatically converts meeting recordings into structured PRDs, JIRA tickets, and action items — built for product managers at Series A+ startups",
        height=110
    )
    col_a, col_b = st.columns(2)
    with col_a:
        audience = st.selectbox("Target Audience", [
            "B2B — Enterprise","B2B — SMBs","B2B — Startups",
            "B2C — Consumers","B2C — Professionals","Developers","Prosumer"
        ])
        timeline = st.selectbox("Launch In", [
            "ASAP (< 1 month)","1-3 months","3-6 months","6-12 months"
        ])
    with col_b:
        budget = st.selectbox("Marketing Budget", [
            "Bootstrap (< $5K)","Seed ($5K-$50K)","Growth ($50K-$500K)","Scale ($500K+)"
        ])
        category = st.selectbox("Category", [
            "Productivity / SaaS","AI Tool","Consumer App",
            "Developer Tool","Marketplace","Fintech","Health","E-Commerce","Other"
        ])
    usp = st.text_area("Your Unique Advantage",
        placeholder="What makes this 10x better than alternatives?", height=65)
    submit = st.button("🚀 Generate GTM Launch Plan")

with col2:
    st.subheader("📋 GTM Launch Plan")

    if submit:
        if not api_key:
            st.error("⚠️ Add your OpenRouter API key (sidebar) — it's free!")
        elif not product_name or not product_desc:
            st.error("⚠️ Fill product name and description")
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
- Exact persona (job title, company, pain point score)
- Where they discover products like this
- Their buying trigger

## 📣 Top 3 Launch Channels
For each: **Channel** | **Tactic** | **Expected reach** | **Est. cost**  
(Tailored to the {budget} budget)

## 📅 Launch Timeline
- **T-4 weeks:** Pre-launch (build waitlist, tease)
- **T-2 weeks:** Soft launch (beta users, feedback)
- **Launch Day:** Exact plan (posts, emails, outreach)
- **T+2 weeks:** Momentum (follow-ups, press, retargeting)

## 💬 Messaging Framework
- Hero headline (under 10 words)
- 3 key messages (one per ICP pain point)
- Primary CTA

## 📊 Launch KPIs
- Week 1 target
- Month 1 target  
- 90-day north star metric

## ⚡ 3 Things To Do This Week
Concrete, specific actions. No vague advice.

Be specific. Include real channels (Product Hunt, Reddit, LinkedIn, etc.) appropriate for the budget and audience."""

            try:
                output_placeholder = st.empty()
                full_response = ""

                with requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://ai-product-launch.streamlit.app",
                        "X-Title": "AI Product Launch Planner"
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
                            "💾 Download Launch Plan (.md)",
                            data=full_response,
                            file_name=f"{product_name.lower().replace(' ','_')}_launch_plan.md",
                            mime="text/markdown"
                        )
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.markdown("""
        <div class="output-box">
<b>What you'll get:</b>

🎯  Sharp positioning statement
👥  Ideal Customer Profile (ICP)
📣  Top channels by budget
📅  Week-by-week launch timeline
💬  Messaging + headline copy
📊  KPIs & 90-day targets
⚡  3 quick wins to do NOW

<b>Works for:</b> SaaS · Apps · Marketplaces · AI tools
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Free AI · OpenRouter · github.com/yourusername/ai-portfolio-apps")
