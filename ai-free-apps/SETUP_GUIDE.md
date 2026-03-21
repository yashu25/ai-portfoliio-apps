# 📖 SEEDHA GUIDE — Free AI Apps Setup
## (Hindi mein — step by step)

---

## PART 1: Free API Key Lena (2 minutes)

1. Jao → **https://openrouter.ai**
2. **"Sign Up"** pe click karo
3. Email + password se account banao
4. Left menu mein **"API Keys"** pe click karo
5. **"Create Key"** → naam kuch bhi likho → Create
6. Key copy karo — `sk-or-v1-...` se shuru hogi
7. ✅ Done! **Koi credit card nahi dena!**

---

## PART 2: GitHub Pe Code Upload Karna

### GitHub Account
1. Jao → **https://github.com**
2. "Sign up" → email/password → account ready

### Naya Repo Banao
1. GitHub pe **"+"** → **"New repository"**
2. Name: `ai-portfolio-apps`
3. **Public** select karo
4. ✅ "Add README" check karo
5. **"Create repository"**

### Files Upload Karo
1. ZIP file extract karo (saari files bahar aayengi)
2. GitHub repo mein **"Add file"** → **"Upload files"**
3. Saari files/folders drag & drop karo
4. **"Commit changes"** → Done! ✅

---

## PART 3: Live Deploy Karna (Free)

### Streamlit Account
1. Jao → **https://share.streamlit.io**
2. **"Sign in with GitHub"** → Allow karo

### App Deploy Karo

**App 1 — Consultant Agent:**
1. **"New app"** pe click karo
2. Repository: `ai-portfolio-apps`
3. Main file path: `consultant_agent/app.py`
4. **"Deploy!"** → 2-3 min wait karo
5. 🎉 **Live link mil gayi!** Kuch aisa: `https://yourname-consultant.streamlit.app`

**App 2 — VC Diligence:**
- Main file path: `vc_diligence/app.py`

**App 3 — Product Launch:**
- Main file path: `product_launch/app.py`

---

## PART 4: App Use Karna

1. Live link kholo
2. **Sidebar mein API key paste karo** (`sk-or-v1-...`)
3. Form bharo
4. Button dabao → **AI ka jawab stream hoga!** ✨

---

## PART 5: Resume Pe Kya Likhna

```
Projects:

AI Portfolio — 3 Production AI Agents           2025
• Built 3 AI tools: Consultant Agent, VC Due Diligence, 
  Product Launch Planner using free LLMs (Llama 3.3, DeepSeek)
• Real-time streaming responses via OpenRouter API
• Deployed live on Streamlit Cloud
• Tech: Python · Streamlit · OpenRouter (free tier)
• GitHub: github.com/[tera-username]/ai-portfolio-apps
• Live: [teri-streamlit-link]
```

---

## PART 6: Koi Problem Aaye?

**"ModuleNotFoundError" dikhe:**
Terminal mein: `pip install streamlit requests`

**"API key invalid" dikhe:**
OpenRouter pe jao → check karo key sahi copy hui ya nahi

**Streamlit deploy fail ho:**
`requirements.txt` file check karo — `streamlit` aur `requests` likha hona chahiye

---

*Koi dikkat aaye toh Claude se pooch!* 🙌
