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

# ---------------- LLM CALL ---------------- #
def call_llm(api_key, model, prompt, placeholder):
    models_to_try = [model] + [m for m in MODELS if m != model]
    for m in models_to_try:
        full = ""
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key.strip()}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": m,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                    "max_tokens": 1800
                },
                stream=True,
                timeout=60
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
                                placeholder.markdown(f'<div class="out">{full}▌</div>', unsafe_allow_html=True)
                        except:
                            pass

            placeholder.markdown(f'<div class="out">{full}</div>', unsafe_allow_html=True)
            return full, m

        except Exception as e:
            if "429" in str(e) or "404" in str(e):
                continue
            raise e

    raise Exception("Models rate-limited. Retry in 2 min.")

# ---------------- FRAMEWORK LOGIC ---------------- #
def get_framework_prompt(framework):

    if "Auto" in framework:
        return "", "3–4 root causes."

    if "MECE" in framework:
        return """
Use strict MECE Issue Tree logic.
Break problem into mutually exclusive, collectively exhaustive buckets.
""", "3–4 MECE root causes."

    if "McKinsey 7S" in framework:
        return """
Use McKinsey 7S Framework:
Strategy, Structure, Systems, Shared Values, Skills, Style, Staff
""", "Analyze across 7S elements."

    if "Jobs To Be Done" in framework:
        return """
Use Jobs To Be Done framework.

Break into:
- Functional Jobs
- Emotional Jobs
- Social Jobs

Identify:
- Hiring triggers
- Pain points
- Desired outcomes
""", "Analyze using JTBD (Functional, Emotional, Social Jobs)."

    if "Porter" in framework:
        return """
Use Porter’s 5 Forces:
- Rivalry
- Supplier Power
- Buyer Power
- Substitutes
- New Entrants
""", "Analyze using Porter’s 5 Forces."

    if "SWOT" in framework:
        return """
Use SWOT:
Strengths, Weaknesses, Opportunities, Threats
""", "Analyze using SWOT."

    return "", "3–4 root causes."

# ---------------- UI ---------------- #

st.set_page_config(page_title="AI Consultant Agent", page_icon="🤝", layout="wide")

with st.sidebar:
    st.title("🤝 AI Consultant")
    st.markdown("Free key → https://openrouter.ai")

    api_key = st.text_input("OpenRouter API Key", type="password")
    model = st.selectbox("Model", MODELS)

# ---------------- MAIN ---------------- #

st.title("AI Consultant Agent")
st.subheader("McKinsey-style analysis")

col1, col2 = st.columns([1, 1.2])

with col1:
    industry = st.selectbox("Industry", [
        "Technology / SaaS","E-Commerce","Healthcare","Finance","Education","Startup","Other"
    ])

    company_size = st.selectbox("Company Size", [
        "Startup","Small","Mid-size","Enterprise"
    ])

    problem = st.text_area("Business Problem")

    framework = st.selectbox("Framework", [
        "Auto — AI picks best fit",
        "MECE + Issue Tree",
        "McKinsey 7S",
        "Jobs To Be Done",
        "Porter's 5 Forces",
        "SWOT + Strategic Options"
    ])

    submit = st.button("Analyze")

# ---------------- OUTPUT ---------------- #

with col2:
    if submit:

        if not api_key or not api_key.startswith("sk-"):
            st.error("Enter valid OpenRouter key (sk-or-v1-...)")

        elif not problem.strip():
            st.error("Enter problem")

        else:
            fw_prompt, rca_section = get_framework_prompt(framework)

            prompt = f"""
You are a senior McKinsey consultant.

STRICT:
- Follow selected framework ONLY
- Do NOT default to MECE unless selected

Client: {industry} | {company_size}
Problem: {problem}

{fw_prompt}

## 🎯 Problem Statement
One crisp sentence.

## 🔍 Root Cause Analysis
{rca_section}

## 💡 Top 3 Recommendations
Each: What | Why | Impact | Effort

## 📅 90-Day Plan
- Weeks 1–2
- Month 1
- Months 2–3

## ⚠️ Risks

## 📈 KPIs
"""

            try:
                out = st.empty()

                with st.spinner("Analyzing..."):
                    full, used = call_llm(api_key, model, prompt, out)

                st.success(f"Generated using {used}")

                st.download_button(
                    "Download",
                    data=full,
                    file_name="analysis.md"
                )

            except Exception as e:
                st.error(str(e))
