import requests
import json

# Models in priority order - if one fails 429, tries next
FALLBACK_MODELS = [
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "deepseek/deepseek-v3-base:free",
    "mistralai/mistral-7b-instruct:free",
    "qwen/qwen3-8b:free",
]

def stream_llm(api_key, model, prompt, placeholder, output_class="output-card"):
    """
    Streams LLM response. Auto-retries with fallback models on 429.
    Returns (full_text, model_used) or raises Exception.
    """
    models_to_try = [model] + [m for m in FALLBACK_MODELS if m != model]

    for attempt_model in models_to_try:
        full = ""
        try:
            with requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://yashconsultsagentically.streamlit.app",
                    "X-Title": "AI Portfolio Apps"
                },
                json={
                    "model": attempt_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                    "max_tokens": 1800,
                },
                stream=True,
                timeout=60
            ) as r:
                if r.status_code == 429:
                    # Rate limited - try next model silently
                    continue
                if r.status_code != 200:
                    error_text = r.text
                    raise Exception(f"API Error {r.status_code}: {error_text}")

                for line in r.iter_lines():
                    if line:
                        line = line.decode("utf-8")
                        if line.startswith("data: ") and line != "data: [DONE]":
                            try:
                                d = json.loads(line[6:])
                                delta = d["choices"][0]["delta"].get("content", "")
                                if delta:
                                    full += delta
                                    placeholder.markdown(
                                        f'<div class="{output_class}">{full}▌</div>',
                                        unsafe_allow_html=True
                                    )
                            except Exception:
                                pass

                placeholder.markdown(
                    f'<div class="{output_class}">{full}</div>',
                    unsafe_allow_html=True
                )
                return full, attempt_model

        except Exception as e:
            if "429" in str(e):
                continue
            raise e

    raise Exception("All free models are rate-limited right now. Please wait 1-2 minutes and try again.")
