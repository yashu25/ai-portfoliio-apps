import streamlit as st
import anthropic

st.set_page_config(
    page_title="AI VC Due Diligence",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #0a0f1a; color: #e8e8f0; }
    .stTextArea textarea { background-color: #111827; color: #e8e8f0; border: 1px solid #1e3a5f; }
    .stTextInput input { background-color: #111827; color: #e8e8f0; border: 1px solid #1e3a5f; }
    .stSelectbox > div > div { background-color: #111827; color: #e8e8f0; }
    .output-box { background-color: #111827; border: 1px solid #3b82f6; border-radius: 10px; padding: 20px; margin-top: 10px; }
    h1 { color: #3b82f6; }
    h2, h3 { color: #60a5fa; }
    .stButton button { background-color: #2563eb; color: white; border: none; border-radius: 8px; font-weight: bold; }
    .metric-box { background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 12px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("📊 AI VC Due Diligence Agent")
st.markdown("*Enter a startup — get an investor-grade due diligence report instantly*")
st.divider()

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🚀 Startup Details")
    
    startup_name = st.text_input("Startup Name", placeholder="e.g. Zepto, Razorpay, Notion...")
    
    one_liner = st.text_area(
        "One-liner / Pitch",
        placeholder="e.g. B2B SaaS for automating accounts payable using AI — helps finance teams reduce invoice processing time by 80%",
        height=80
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        stage = st.selectbox("Stage", ["Pre-seed", "Seed", "Series A", "Series B", "Series C+", "Growth"])
        sector = st.selectbox("Sector", [
            "Fintech", "Healthtech", "Edtech", "SaaS / B2B", "Consumer", 
            "D2C", "Deeptech / AI", "Climatetech", "Logistics", "Other"
        ])
    with col_b:
        geography = st.selectbox("Geography", ["India", "USA", "SEA", "Europe", "Global", "Other"])
        revenue = st.selectbox("Revenue Stage", [
            "Pre-revenue", "< $100K ARR", "$100K-$1M ARR", "$1M-$10M ARR", "$10M+ ARR"
        ])
    
    extra = st.text_area(
        "Additional Context (optional)",
        placeholder="Team background, traction, competitors, key metrics...",
        height=80
    )
    
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    submit = st.button("🔍 Run Due Diligence", use_container_width=True)

with col2:
    st.subheader("📋 Due Diligence Report")
    
    if submit:
        if not api_key:
            st.error("⚠️ Please enter your Anthropic API key")
        elif not startup_name or not one_liner:
            st.error("⚠️ Please fill startup name and pitch")
        else:
            prompt = f"""You are a General Partner at a top-tier VC firm (think Sequoia, Accel, a16z). 
Perform a rigorous due diligence on this startup:

Startup: {startup_name}
Pitch: {one_liner}
Stage: {stage} | Sector: {sector} | Geography: {geography} | Revenue: {revenue}
Additional Info: {extra if extra else 'Not provided'}

Generate a complete VC due diligence report:

## 🎯 Investment Thesis (2-3 sentences — why this could be big)

## 🌊 Market Analysis
- TAM / SAM / SOM estimate with reasoning
- Market timing — why now?
- Key tailwinds

## ⚔️ Competitive Landscape
- Direct & indirect competitors
- Differentiation / moat assessment
- Defensibility score: [X/10] with reasoning

## 💰 Business Model Analysis
- Revenue model clarity
- Unit economics (estimated)
- Scalability assessment

## 🚨 Key Risks (Top 5)
For each: Risk | Severity (H/M/L) | Mitigation

## 🔑 Key Questions for Founders (Top 5 DD questions)

## ✅ Investment Verdict
- Recommendation: PASS / WATCH / INVEST
- Valuation range (if invest)
- Key conditions / next steps

Be direct. Use data where possible. Think like a skeptical but open-minded investor."""

            client = anthropic.Anthropic(api_key=api_key)
            
            with st.spinner(f"Running due diligence on {startup_name}..."):
                output_placeholder = st.empty()
                full_response = ""
                
                with client.messages.stream(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1800,
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
                    "💾 Download DD Report (.md)",
                    data=full_response,
                    file_name=f"{startup_name.lower().replace(' ', '_')}_due_diligence.md",
                    mime="text/markdown"
                )
    else:
        st.markdown("""
        <div class="output-box">
        <h3>📊 What you'll get</h3>
        <ul>
        <li>📈 Market sizing (TAM/SAM/SOM)</li>
        <li>⚔️ Competitive analysis & moat score</li>
        <li>💰 Business model & unit economics</li>
        <li>🚨 Risk assessment (Top 5)</li>
        <li>🔑 Key DD questions for founders</li>
        <li>✅ Investment verdict with reasoning</li>
        </ul>
        <br>
        <p>Try with any startup: <strong>Zepto, Razorpay, Notion, Linear</strong> — or your own idea!</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Built with Claude AI · Inspired by awesome-llm-apps · github.com/yourusername")
