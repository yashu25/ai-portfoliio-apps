import streamlit as st
import anthropic

st.set_page_config(
    page_title="AI Product Launch Planner",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #0a0f0f; color: #e8e8f0; }
    .stTextArea textarea { background-color: #0f1f1f; color: #e8e8f0; border: 1px solid #0d4f4f; }
    .stTextInput input { background-color: #0f1f1f; color: #e8e8f0; border: 1px solid #0d4f4f; }
    .stSelectbox > div > div { background-color: #0f1f1f; color: #e8e8f0; }
    .output-box { background-color: #0f1f1f; border: 1px solid #10b981; border-radius: 10px; padding: 20px; margin-top: 10px; }
    h1 { color: #10b981; }
    h2, h3 { color: #34d399; }
    .stButton button { background-color: #059669; color: white; border: none; border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Product Launch Planner")
st.markdown("*Describe your product idea — get a full GTM launch plan in seconds*")
st.divider()

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📦 Product Details")
    
    product_name = st.text_input("Product Name", placeholder="e.g. TaskFlow, BeatSync, MediScan...")
    
    product_desc = st.text_area(
        "What does it do?",
        placeholder="e.g. An AI tool that automatically converts meeting recordings into structured PRDs, JIRA tickets, and action items for product teams",
        height=100
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        target_audience = st.selectbox("Primary Target", [
            "B2B — Enterprise", "B2B — SMBs", "B2B — Startups",
            "B2C — Consumers", "B2C — Gen Z", "B2C — Professionals",
            "Developer Tools", "Prosumer"
        ])
        launch_timeline = st.selectbox("Launch Timeline", [
            "ASAP (< 1 month)", "1-3 months", "3-6 months", "6-12 months"
        ])
    with col_b:
        budget = st.selectbox("Marketing Budget", [
            "Bootstrap (< $5K)", "Seed ($5K-$50K)", "Growth ($50K-$500K)", "Scale ($500K+)"
        ])
        category = st.selectbox("Category", [
            "Productivity / SaaS", "Consumer App", "Developer Tool",
            "Marketplace", "AI / ML", "Fintech", "Health", "E-Commerce", "Other"
        ])
    
    usp = st.text_area(
        "Key Differentiator / USP",
        placeholder="What makes this 10x better than existing solutions?",
        height=60
    )
    
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    submit = st.button("🚀 Generate Launch Plan", use_container_width=True)

with col2:
    st.subheader("📋 GTM Launch Plan")
    
    if submit:
        if not api_key:
            st.error("⚠️ Please enter your Anthropic API key")
        elif not product_name or not product_desc:
            st.error("⚠️ Please fill product name and description")
        else:
            prompt = f"""You are a world-class Product Marketing Manager who has launched products at Stripe, Notion, and Linear.

Product: {product_name}
Description: {product_desc}
Target: {target_audience} | Category: {category}
Timeline: {launch_timeline} | Budget: {budget}
USP: {usp if usp else 'Not specified'}

Create a complete Go-To-Market launch plan:

## 🎯 Positioning Statement
One crisp sentence: "For [target], {product_name} is the [category] that [key benefit] unlike [alternatives]."

## 👥 Ideal Customer Profile (ICP)
- Who exactly (job title, company type, pain point)
- Where they hang out (channels)
- What triggers them to buy

## 📣 Launch Channels & Tactics
Prioritized by ROI for the given budget:
1. Channel | Tactic | Expected reach | Cost
2. Channel | Tactic | Expected reach | Cost
3. Channel | Tactic | Expected reach | Cost

## 📅 Launch Timeline
- T-4 weeks: Pre-launch (build anticipation)
- T-2 weeks: Soft launch (early access)
- T-0: Public launch day plan
- T+2 weeks: Post-launch momentum

## 💬 Messaging Framework
- Hero headline
- 3 key messages (one per ICP pain point)
- CTA

## 📊 Launch KPIs & Goals
- Week 1 targets
- Month 1 targets
- 90-day north star metric

## ⚡ 3 Quick Wins (do this week)

Be specific. Include real tactics, not vague advice. Think Product Hunt, communities, content, paid — whatever fits the budget."""

            client = anthropic.Anthropic(api_key=api_key)
            
            with st.spinner(f"Building launch plan for {product_name}..."):
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
                    "💾 Download Launch Plan (.md)",
                    data=full_response,
                    file_name=f"{product_name.lower().replace(' ', '_')}_launch_plan.md",
                    mime="text/markdown"
                )
    else:
        st.markdown("""
        <div class="output-box">
        <h3>🚀 What you'll get</h3>
        <ul>
        <li>🎯 Sharp positioning statement</li>
        <li>👥 Ideal Customer Profile (ICP)</li>
        <li>📣 Top channels & tactics (by budget)</li>
        <li>📅 Week-by-week launch timeline</li>
        <li>💬 Messaging framework + headlines</li>
        <li>📊 KPIs & 90-day goals</li>
        <li>⚡ 3 quick wins to do NOW</li>
        </ul>
        <br>
        <p>Works for any product: <strong>SaaS, app, marketplace, AI tool</strong></p>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("Built with Claude AI · Inspired by awesome-llm-apps · github.com/yourusername")
