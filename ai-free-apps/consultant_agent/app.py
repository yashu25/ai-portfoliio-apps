import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Consultant Agent", page_icon="🤝", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0a0a0f; color: #e8e8f0; }
.stTextArea textarea { background-color: #111118; color: #e8e8f0; border: 1px solid #2a2a3f; }
.stTextInput input { background-color: #111118; color: #e8e8f0; border: 1px solid #2a2a3f; }
.stSelectbox > div > div { background-color: #111118; }
.output-box { background-color: #111118; border: 1px solid #7c6af7; border-radius: 10px; padding: 20px; margin-top: 10px; white-space: pre-wrap; font-size: 0.9rem; line-height: 1.7; }
h1 { color: #7c6af7 !important; }
.stButton > button { background: linear-gradient(135deg,#7c6af7,#9b89ff); color: white; border: none; border-radius: 8px; font-weight: bold; width: 100%; }
.stButton > button:hover { filter: brightness(1.1); }
.free-badge { background: rgba(106,247,212,0.1); border: 1px solid rgba(106,247,212,0.3); color: #6af7d4; padding: 4px 12px; border-radius: 100px; font-size: 0.75rem; display: inline-block; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

st.title("🤝 AI Consultant Agent")
st.markdown('<span class="free-badge">✓ 100% FREE — Powered by Llama 3.3 via OpenRouter</span>', unsafe_allow_html=True)
st.markdown("*Describe your business problem → Get a McKinsey-style analysis instantly*")
st.divider()

# --- SIDEBAR: API Key + Model ---
with st.sidebar:
    st.header("⚙️ Setup")
    st.markdown("""
    **Step 1:** Get free API key  
    👉 [openrouter.ai](https://openrouter.ai) → Sign up → API Keys  
    *(No credit card needed!)*
    """)
    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-v1-...")
    
    model = st.selectbox("AI Model (all free)", [
        "meta-llama/llama-3.3-70b-instruct:free",
        "deepseek/deepseek-v3-base:free",
        "google/gemma-3-27b-it:free",
        "mistralai/mistral-7b-instruct:free",
        "qwen/qwen3-8b:free",
    ])
    
    st.divider()
    st.markdown("**Free tier limits:**  \n20 req/min · 200 req/day  \n*(More than enough!)*")

col1, col2 = st.columns([1, 1.1])

with col1:
    st.subheader("📋 Your Problem")
    
    industry = st.selectbox("Industry", [
        "Technology / SaaS", "E-Commerce / Retail", "Healthcare",
        "Finance / Fintech", "Education", "Manufacturing",
        "Consulting / Services", "Startup", "Other"
    ])
    company_size = st.selectbox("Company Size", [
        "Startup (1-10)", "Small (11-50)", "Mid-size (51-500)", "Enterprise (500+)"
    ])
    problem = st.text_area(
        "Describe your business problem in detail",
        placeholder="e.g. Our SaaS product has 30% monthly churn. Freemium conversion is only 3%. Competitors are undercutting our pricing. What should we do?",
        height=200
    )
    framework = st.selectbox("Framework", [
        "Auto (AI decides best)", "MECE + Issue Tree",
        "McKinsey 7S", "Jobs To Be Done",
        "Porter's 5 Forces", "SWOT + Options"
    ])
    submit = st.button("🚀 Analyze with AI Consultant")

with col2:
    st.subheader("📊 Consulting Analysis")

    if submit:
        if not api_key:
            st.error("⚠️ Add your OpenRouter API key in the sidebar (it's free!)")
        elif not problem.strip():
            st.error("⚠️ Please describe your business problem")
        else:
            fw = "" if "Auto" in framework else f"Use the {framework} framework."
            prompt = f"""You are a senior partner at McKinsey & Company with 15 years of experience.

Client:
- Industry: {industry}
- Size: {company_size}  
- Problem: {problem}
{fw}

Deliver a structured consulting analysis:

## 🎯 Problem Statement
One crisp, precise sentence.

## 🔍 Root Cause Analysis
3-4 key root causes (MECE — no overlap, no gaps).

## 💡 Top 3 Strategic Recommendations
For each: **What** | **Why** | **Impact** | **Effort (H/M/L)**

## 📅 90-Day Action Plan
- **Weeks 1-2:** Quick wins (do immediately)
- **Month 1:** Foundation work
- **Months 2-3:** Scale & optimize

## ⚠️ Key Risks & Mitigations
Top 3 risks with mitigation for each.

## 📈 Success Metrics
4-5 KPIs to track progress.

Be specific, direct, and actionable. No fluff. Think like a senior consultant billing $500/hour."""

            try:
                output_placeholder = st.empty()
                full_response = ""

                with requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://ai-consultant-agent.streamlit.app",
                        "X-Title": "AI Consultant Agent"
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": True,
                        "max_tokens": 1500,
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
                                        delta = data["choices"][0]["delta"].get("content", "")
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
                            "💾 Download Analysis (.md)",
                            data=full_response,
                            file_name="consulting_analysis.md",
                            mime="text/markdown"
                        )
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.markdown("""
        <div class="output-box">
<b>How it works:</b>

1️⃣  Add your free OpenRouter API key (sidebar)
2️⃣  Describe your business problem
3️⃣  Click Analyze → get McKinsey-style output

<b>Example problems:</b>
• High customer churn in SaaS product
• Market entry strategy for new product  
• Pricing strategy optimization
• Org restructuring for growth
• Revenue diversification plan
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Free AI · Llama 3.3 70B via OpenRouter · github.com/yourusername/ai-portfolio-apps")
