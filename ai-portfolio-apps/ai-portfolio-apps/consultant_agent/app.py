import streamlit as st
import anthropic

st.set_page_config(
    page_title="AI Consultant Agent",
    page_icon="🤝",
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #0f0f1a; }
    .stApp { background-color: #0f0f1a; color: #e8e8f0; }
    .stTextArea textarea { background-color: #1a1a2e; color: #e8e8f0; border: 1px solid #333; }
    .stSelectbox select { background-color: #1a1a2e; color: #e8e8f0; }
    .output-box { background-color: #1a1a2e; border: 1px solid #7c6af7; border-radius: 10px; padding: 20px; margin-top: 10px; }
    h1 { color: #7c6af7; }
    h2, h3 { color: #a89aff; }
    .stButton button { background-color: #7c6af7; color: white; border: none; border-radius: 8px; font-weight: bold; }
    .stButton button:hover { background-color: #9b89ff; }
</style>
""", unsafe_allow_html=True)

st.title("🤝 AI Consultant Agent")
st.markdown("*Describe your business problem — get a structured consulting framework instantly*")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Problem Brief")
    
    industry = st.selectbox("Industry", [
        "Technology / SaaS", "E-Commerce / Retail", "Healthcare", "Finance / Fintech",
        "Education / Edtech", "Manufacturing", "Consulting / Services", "Startup / Early Stage", "Other"
    ])
    
    company_size = st.selectbox("Company Size", [
        "Startup (1-10)", "Small (11-50)", "Mid-size (51-500)", "Enterprise (500+)"
    ])
    
    problem = st.text_area(
        "Describe your business problem",
        placeholder="e.g. Our SaaS product has high churn — 30% of users drop off after the first month. We have a freemium model and our conversion to paid is only 3%. What should we do?",
        height=180
    )
    
    framework = st.selectbox("Preferred Framework", [
        "Auto (AI decides)", "McKinsey 7S", "MECE + Issue Tree", "Jobs To Be Done", 
        "Porter's 5 Forces", "SWOT + Strategic Options", "OKR Alignment"
    ])
    
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    
    submit = st.button("🚀 Analyze with AI Consultant", use_container_width=True)

with col2:
    st.subheader("📊 Consulting Analysis")
    
    if submit:
        if not api_key:
            st.error("⚠️ Please enter your Anthropic API key")
        elif not problem:
            st.error("⚠️ Please describe your business problem")
        else:
            framework_instruction = "" if framework == "Auto (AI decides)" else f"Use the {framework} framework."
            
            prompt = f"""You are a senior management consultant from McKinsey & Company with 15 years of experience.

Client Context:
- Industry: {industry}
- Company Size: {company_size}
- Problem: {problem}

{framework_instruction}

Provide a structured consulting analysis with:

## 🎯 Problem Statement (1 crisp sentence)

## 🔍 Root Cause Analysis (3-4 key root causes, MECE)

## 💡 Strategic Recommendations (Top 3, prioritized)
For each: What to do | Why | Expected Impact | Effort Level

## 📅 90-Day Action Plan
- Week 1-2: Quick wins
- Month 1: Foundation
- Month 2-3: Scale

## ⚠️ Key Risks & Mitigations

## 📈 Success Metrics (how to measure progress)

Be specific, actionable, and data-driven. No fluff."""

            client = anthropic.Anthropic(api_key=api_key)
            
            with st.spinner("Analyzing your problem..."):
                output_placeholder = st.empty()
                full_response = ""
                
                with client.messages.stream(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1500,
                    messages=[{"role": "user", "content": prompt}]
                ) as stream:
                    for text in stream.text_stream:
                        full_response += text
                        output_placeholder.markdown(
                            f'<div class="output-box">{full_response}▌</div>',
                            unsafe_allow_html=True
                        )
                
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
    else:
        st.markdown("""
        <div class="output-box">
        <h3>How it works</h3>
        <p>1. Describe your business problem in detail<br>
        2. Select your industry & company context<br>
        3. Choose a consulting framework (or let AI decide)<br>
        4. Get a structured McKinsey-style analysis in seconds</p>
        <br>
        <p><strong>Example problems:</strong></p>
        <ul>
        <li>High customer churn in SaaS</li>
        <li>Market entry strategy for new product</li>
        <li>Org structure for scaling team</li>
        <li>Pricing strategy optimization</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Built with Claude AI · Inspired by awesome-llm-apps · github.com/yourusername")
