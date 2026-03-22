import streamlit as st
import requests
import json

# ── FREE MODELS (auto-fallback on 429/404) ──
MODELS = [
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "qwen/qwen3-8b:free",
    "microsoft/phi-3-mini-128k-instruct:free",
]

def call_llm(api_key, prompt, placeholder=None, output_class="out", max_tokens=1500):
    for m in MODELS:
        full = ""
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://yashconsultsagentically.streamlit.app",
                    "X-Title": "AI Competitor Intelligence"
                },
                json={
                    "model": m,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                    "max_tokens": max_tokens
                },
                stream=True, timeout=90
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
                                if placeholder:
                                    placeholder.markdown(
                                        f'<div class="{output_class}">{full}▌</div>',
                                        unsafe_allow_html=True
                                    )
                        except: pass
            if placeholder:
                placeholder.markdown(f'<div class="{output_class}">{full}</div>', unsafe_allow_html=True)
            return full, m
        except Exception as e:
            if "429" in str(e) or "404" in str(e): continue
            raise e
    raise Exception("All free models are rate-limited. Please wait 1-2 minutes and retry.")

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="AI Competitor Intelligence Agent Team",
    page_icon="🧲",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: #F8F6FF; color: #1a0a2e; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1300px !important; }

[data-testid="stSidebar"] { background: #1a0a2e !important; }
[data-testid="stSidebar"] * { color: #e8e0f0 !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #e8e0f0 !important; border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important;
}
[data-testid="stSidebar"] label { color: rgba(255,255,255,0.45) !important; font-size: 0.68rem !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
[data-testid="stSidebar"] a { color: #c084fc !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; }

.page-tag { display: inline-flex; align-items: center; gap: 6px; background: #1a0a2e; color: #c084fc; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 1.5px; text-transform: uppercase; padding: 5px 14px; border-radius: 100px; margin-bottom: 16px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 800; color: #1a0a2e; line-height: 1.15; margin-bottom: 10px; }
.page-title span { color: #7c3aed; }
.page-sub { font-size: 0.98rem; color: #6b5b80; line-height: 1.6; margin-bottom: 8px; }
.divider { border: none; border-top: 1px solid #e2d9f0; margin: 0 0 28px; }

.sec-label { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; letter-spacing: 2px; text-transform: uppercase; color: #9c7ab8; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }
.sec-label::after { content: ''; flex: 1; height: 1px; background: #e2d9f0; }

.stTextArea textarea { background: white !important; border: 1.5px solid #e2d9f0 !important; border-radius: 12px !important; color: #1a0a2e !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; line-height: 1.75 !important; padding: 14px 16px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
.stTextArea textarea:focus { border-color: #7c3aed !important; box-shadow: 0 0 0 3px rgba(124,58,237,0.08) !important; }
.stTextArea textarea::placeholder { color: #c5b8d8 !important; }
.stSelectbox > div > div { background: white !important; border: 1.5px solid #e2d9f0 !important; border-radius: 10px !important; color: #1a0a2e !important; font-size: 0.88rem !important; }
.stTextInput input { background: white !important; border: 1.5px solid #e2d9f0 !important; border-radius: 10px !important; color: #1a0a2e !important; font-size: 0.88rem !important; }
label { font-size: 0.78rem !important; font-weight: 600 !important; color: #374151 !important; }

.stButton > button { background: #1a0a2e !important; color: white !important; border: none !important; border-radius: 12px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.92rem !important; font-weight: 600 !important; padding: 14px 28px !important; width: 100% !important; box-shadow: 0 4px 16px rgba(26,10,46,0.25) !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #2d1a4e !important; transform: translateY(-1px) !important; }

/* Agent cards */
.agent-header { display: flex; align-items: center; gap: 12px; margin: 24px 0 12px; padding-bottom: 12px; border-bottom: 1px solid #e2d9f0; }
.agent-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; padding: 3px 10px; border-radius: 100px; letter-spacing: 0.5px; font-weight: 600; }
.badge-finder   { background: #fef3c7; color: #92400e; }
.badge-analyst  { background: #dbeafe; color: #1e40af; }
.badge-compare  { background: #d1fae5; color: #065f46; }
.badge-strategy { background: #fce7f3; color: #9d174d; }
.agent-name { font-family: 'Playfair Display', serif; font-size: 1rem; font-weight: 700; color: #1a0a2e; }

.out { background: white; border: 1.5px solid #e2d9f0; border-radius: 16px; padding: 24px 28px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.9rem; line-height: 1.85; color: #374151; box-shadow: 0 4px 24px rgba(0,0,0,0.06); margin-bottom: 8px; }
.out-finder   { border-left: 4px solid #f59e0b; }
.out-analyst  { border-left: 4px solid #3b82f6; }
.out-compare  { border-left: 4px solid #10b981; }
.out-strategy { border-left: 4px solid #ec4899; }

.pipeline { display: flex; align-items: center; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.pipeline-step { background: white; border: 1.5px solid #e2d9f0; border-radius: 10px; padding: 7px 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #6b5b80; letter-spacing: 0.5px; }
.pipeline-step.active { background: #1a0a2e; color: white; border-color: #1a0a2e; }
.pipeline-arrow { color: #c084fc; font-size: 1rem; }

.empty-box { background: white; border: 1.5px dashed #d8c8f0; border-radius: 16px; padding: 52px 36px; text-align: center; }
.empty-box .icon { font-size: 2.8rem; margin-bottom: 14px; }
.empty-box h3 { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #6b5b80; font-weight: 700; margin-bottom: 8px; }
.empty-box p { font-size: 0.85rem; color: #9c7ab8; line-height: 1.7; margin-bottom: 18px; }
.tag { display: inline-block; background: #f3e8ff; color: #7c3aed; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; padding: 4px 11px; border-radius: 6px; margin: 3px; }

.stDownloadButton > button { background: white !important; color: #374151 !important; border: 1.5px solid #e2d9f0 !important; border-radius: 10px !important; font-size: 0.82rem !important; width: 100% !important; margin-top: 8px !important; box-shadow: none !important; }
.stDownloadButton > button:hover { border-color: #7c3aed !important; color: #7c3aed !important; }
.footer { margin-top: 48px; padding-top: 20px; border-top: 1px solid #e2d9f0; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #c5b8d8; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:28px 20px 20px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:16px;">
        <div style="font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;color:white;margin-bottom:5px;">🧲 Competitor Intel</div>
        <div style="font-size:0.72rem;color:rgba(255,255,255,0.38);line-height:1.6;">4 AI agents · Inspired by<br>awesome-llm-apps (96k ⭐)</div>
        <div style="background:rgba(192,132,252,0.18);border:1px solid rgba(192,132,252,0.28);color:#c084fc;font-family:'JetBrains Mono',monospace;font-size:0.6rem;padding:3px 10px;border-radius:100px;margin-top:12px;display:inline-block;">✦ MULTI-AGENT · FREE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="font-size:0.72rem;color:rgba(255,255,255,0.38);line-height:1.7;padding:0 4px 12px;">
    Free key → <a href="https://openrouter.ai" target="_blank">openrouter.ai</a><br>
    Sign up → API Keys → Create
    </div>""", unsafe_allow_html=True)

    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-v1-...")

    st.divider()
    st.markdown("""<div style="font-size:0.7rem;color:rgba(255,255,255,0.28);line-height:1.9;padding:0 4px;">
    <b style="color:rgba(255,255,255,0.5);">Agent Pipeline:</b><br>
    🔍 Agent 1: Competitor Finder<br>
    📊 Agent 2: Deep Analyst<br>
    ⚖️ Agent 3: Comparison Engine<br>
    ♟️ Agent 4: Strategist
    </div>""", unsafe_allow_html=True)

# ── MAIN ──
st.markdown('<div class="page-tag">✦ 4-Agent Pipeline · Free · Inspired by awesome-llm-apps</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">🧲 AI Competitor Intelligence <span>Agent Team</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Enter your company URL or description — 4 AI agents find competitors, analyze them, compare, and recommend your strategy.</div>', unsafe_allow_html=True)
st.info("For best results, provide both your company URL and a short description!")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.markdown('<div class="sec-label">Your Company</div>', unsafe_allow_html=True)
    url = st.text_input("Company URL", placeholder="e.g. https://notion.so")
    description = st.text_area(
        "Company Description",
        placeholder="e.g. All-in-one workspace for notes, docs, wikis and project management for teams",
        height=100
    )
    industry = st.selectbox("Industry", [
        "SaaS / B2B", "Fintech", "E-Commerce", "Healthtech",
        "Edtech", "Consumer App", "Marketplace", "D2C", "Other"
    ])
    num_competitors = st.selectbox("Competitors to analyze", [2, 3, 4])
    submit = st.button("🚀 Launch 4-Agent Analysis →")

with col2:
    st.markdown('<div class="sec-label">Agent Pipeline Output</div>', unsafe_allow_html=True)

    if submit:
        if not api_key:
            st.error("⚠️ Add your OpenRouter API key in the sidebar — free at openrouter.ai")
        elif not url and not description:
            st.error("⚠️ Please provide at least your company URL or description.")
        else:
            full_report = ""
            company_context = f"URL: {url}" if url else ""
            if description:
                company_context += f"\nDescription: {description}"

            # ══ AGENT 1: COMPETITOR FINDER ══
            st.markdown("""
            <div class="pipeline">
                <div class="pipeline-step active">🔍 Agent 1</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step">📊 Agent 2</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step">⚖️ Agent 3</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step">♟️ Agent 4</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""<div class="agent-header">
                <span class="agent-badge badge-finder">AGENT 1</span>
                <span class="agent-name">🔍 Competitor Finder</span>
            </div>""", unsafe_allow_html=True)

            p1 = st.empty()
            with st.spinner("Agent 1 finding competitors..."):
                prompt1 = f"""You are a market research expert. A company has provided the following details:

{company_context}
Industry: {industry}

Your task: Identify the top {num_competitors} direct competitors for this company.

For each competitor provide:

## Competitor [N]: [Company Name]
- **Website:** [URL]
- **What they do:** 1-2 sentence description
- **Why they compete:** How they directly compete with the input company
- **Company stage:** (Startup / Growth / Enterprise)
- **Estimated market presence:** (Niche / Regional / Global)

Be specific. Only list real, known companies that are actual competitors in this space."""

                finder_output, _ = call_llm(api_key, prompt1, p1, "out out-finder", 1000)
                full_report += f"# AGENT 1: COMPETITOR FINDER\n\n{finder_output}\n\n---\n\n"

            # ══ AGENT 2: DEEP ANALYST ══
            st.markdown("""
            <div class="pipeline" style="margin-top:8px;">
                <div class="pipeline-step">🔍 Agent 1</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step active">📊 Agent 2</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step">⚖️ Agent 3</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step">♟️ Agent 4</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""<div class="agent-header">
                <span class="agent-badge badge-analyst">AGENT 2</span>
                <span class="agent-name">📊 Deep Analyst</span>
            </div>""", unsafe_allow_html=True)

            p2 = st.empty()
            with st.spinner("Agent 2 doing deep analysis..."):
                prompt2 = f"""You are a competitive intelligence analyst. Based on these competitors identified for a {industry} company:

{finder_output}

Perform a deep analysis of each competitor:

For each competitor analyze:

## [Company Name] — Deep Analysis

**Pricing & Plans**
Describe known pricing tiers, free vs paid, enterprise pricing approach.

**Key Features & Capabilities**
List 5 most important product features/capabilities.

**Tech Stack & Infrastructure**
Known technologies, platforms, integrations they offer.

**Marketing & Positioning**
How do they position themselves? What's their core message? Who do they target?

**Strengths** (Top 3)
**Weaknesses & Gaps** (Top 3)

**Customer Sentiment**
What do customers love? What do they complain about? (Based on known market feedback)

Be detailed and specific. Use your knowledge of these companies."""

                analyst_output, _ = call_llm(api_key, prompt2, p2, "out out-analyst", 1500)
                full_report += f"# AGENT 2: DEEP ANALYSIS\n\n{analyst_output}\n\n---\n\n"

            # ══ AGENT 3: COMPARISON ENGINE ══
            st.markdown("""
            <div class="pipeline" style="margin-top:8px;">
                <div class="pipeline-step">🔍 Agent 1</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step">📊 Agent 2</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step active">⚖️ Agent 3</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step">♟️ Agent 4</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""<div class="agent-header">
                <span class="agent-badge badge-compare">AGENT 3</span>
                <span class="agent-name">⚖️ Comparison Engine</span>
            </div>""", unsafe_allow_html=True)

            p3 = st.empty()
            with st.spinner("Agent 3 building comparison matrix..."):
                prompt3 = f"""You are a product strategy expert. Based on this analysis of competitors for a {industry} company:

Our Company: {company_context}

COMPETITOR ANALYSIS:
{analyst_output[:1500]}

Build a structured comparison:

## Head-to-Head Comparison Matrix

| Dimension | Our Company | {f'Competitor 1' if num_competitors >= 1 else ''} | {f'Competitor 2' if num_competitors >= 2 else ''} | {f'Competitor 3' if num_competitors >= 3 else ''} |
|-----------|-------------|--------------|--------------|--------------|
| Pricing Model | ? | ... | ... | ... |
| Core Strength | ? | ... | ... | ... |
| Target Customer | ? | ... | ... | ... |
| Product Depth | ? | ... | ... | ... |
| Ease of Use | ? | ... | ... | ... |
| Integrations | ? | ... | ... | ... |
| Support Quality | ? | ... | ... | ... |

(Fill in based on analysis. Mark "?" for our company where unknown.)

## Market Gap Analysis
Top 3 gaps NONE of the competitors are filling well.

## Where We Can Win
Specific segments or use cases where our company has a clear path to winning.

## Where We Are Vulnerable
Honest assessment of where competitors have the advantage.

## Threat Level Assessment
Rate each competitor: LOW / MEDIUM / HIGH threat with 1-line reason."""

                compare_output, _ = call_llm(api_key, prompt3, p3, "out out-compare", 1500)
                full_report += f"# AGENT 3: COMPARISON MATRIX\n\n{compare_output}\n\n---\n\n"

            # ══ AGENT 4: STRATEGIST ══
            st.markdown("""
            <div class="pipeline" style="margin-top:8px;">
                <div class="pipeline-step">🔍 Agent 1</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step">📊 Agent 2</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step">⚖️ Agent 3</div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step active">♟️ Agent 4</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""<div class="agent-header">
                <span class="agent-badge badge-strategy">AGENT 4</span>
                <span class="agent-name">♟️ Strategic Advisor</span>
            </div>""", unsafe_allow_html=True)

            p4 = st.empty()
            with st.spinner("Agent 4 building strategy..."):
                prompt4 = f"""You are a Chief Strategy Officer. Based on the complete competitive intelligence gathered:

Our Company: {company_context}
Industry: {industry}

COMPARISON & GAPS:
{compare_output[:1200]}

Deliver the complete strategic playbook:

## Executive Summary
3 sentences: situation, opportunity, recommended direction.

## Strategic Recommendation
Clear directive: Attack / Differentiate / Niche Down / Partner / Expand

## 6 Market Opportunities to Capitalize On
Specific, actionable opportunities ranked by impact.

## 90-Day Competitive Battle Plan
- **Month 1 — Quick Wins:** (immediate actions)
- **Month 2 — Positioning:** (product & marketing moves)
- **Month 3 — Moat Building:** (defensibility plays)

## Winning Messaging Against Each Competitor
For each competitor: the 1 key message to use when prospects mention them.

## Product Roadmap Recommendations
5 features/improvements that would create competitive advantage.

## Pricing Strategy
Recommended approach to pricing vs competitors.

## Success Metrics
5 KPIs to track whether the strategy is working.

This should be boardroom-ready. Be bold, specific, and actionable."""

                strategy_output, used_model = call_llm(api_key, prompt4, p4, "out out-strategy", 1500)
                full_report += f"# AGENT 4: STRATEGIC PLAYBOOK\n\n{strategy_output}"

            st.caption(f"✓ Analysis complete · Powered by `{used_model}`")
            st.download_button(
                "⬇ Download Full Intelligence Report (.md)",
                data=full_report,
                file_name=f"competitor_intelligence_report.md",
                mime="text/markdown"
            )

    else:
        st.markdown(f"""
        <div class="empty-box">
            <div class="icon">🧲</div>
            <h3>4 agents ready to deploy</h3>
            <p>Enter your company details on the left.<br>All 4 agents will run in sequence automatically.</p>
            <div>
                <span class="tag">🔍 Find Competitors</span>
                <span class="tag">📊 Deep Analysis</span>
                <span class="tag">⚖️ Comparison Matrix</span>
                <span class="tag">♟️ Strategic Playbook</span>
                <span class="tag">90-Day Battle Plan</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="footer">Inspired by Shubham Saboo\'s awesome-llm-apps (96k ⭐) · Converted to free OpenRouter stack · Streamlit</div>', unsafe_allow_html=True)
