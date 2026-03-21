# 📖 SEEDHA GUIDE — GitHub Pe Upload & Deploy Karna
## (Non-technical logon ke liye — Hindi mein)

---

## PART 1: GitHub Pe Code Upload Karna

### Step 1: GitHub Account Banao
1. Jao → https://github.com
2. "Sign up" pe click karo
3. Username, email, password daalo → Account ban jayega

---

### Step 2: Naya Repository Banao
1. GitHub pe login karo
2. Upar right mein **"+"** icon pe click karo → "New repository"
3. Repository name likho: `ai-portfolio-apps`
4. "Public" select karo (important!)
5. ✅ "Add a README file" check karo
6. **"Create repository"** pe click karo

---

### Step 3: Files Upload Karo
1. Apne repository page pe jao
2. **"Add file"** button pe click karo → **"Upload files"**
3. Download ki gayi ZIP file extract karo
4. Saari files drag & drop karo yahan
5. Neeche **"Commit changes"** pe click karo
6. ✅ Done! Code GitHub pe aa gaya!

---

## PART 2: App Deploy Karna (Live Link Milegi)

### Step 1: Streamlit Account Banao
1. Jao → https://share.streamlit.io
2. **"Sign in with GitHub"** pe click karo
3. Allow karo → Account connect ho jayega

---

### Step 2: App Deploy Karo

**Consultant Agent ke liye:**
1. https://share.streamlit.io pe jao
2. **"New app"** pe click karo
3. Repository: `ai-portfolio-apps` select karo
4. Main file path mein likho: `consultant_agent/app.py`
5. **"Deploy!"** pe click karo
6. 2-3 minutes wait karo → **Live link mil jayegi!** 🎉

**Yahi repeat karo VC Diligence ke liye:**
- Main file path: `vc_diligence/app.py`

**Aur Product Launch ke liye:**
- Main file path: `product_launch/app.py`

---

## PART 3: Resume Pe Kaise Likhna

```
Projects:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI Portfolio — 3 Production AI Agents          2025
• Built 3 AI-powered tools using Claude API (Anthropic) and Streamlit
• AI Consultant Agent: Generates McKinsey-style analysis from business problems
• VC Due Diligence Agent: Produces investor-grade startup analysis reports  
• Product Launch Planner: Creates complete GTM plans from product ideas
• Deployed live on Streamlit Cloud with real-time AI streaming
• Tech: Python, Anthropic Claude API, Streamlit
• GitHub: github.com/yourusername/ai-portfolio-apps
• Live: your-app.streamlit.app
```

---

## PART 4: API Key Kahan Se Milegi?

1. Jao → https://console.anthropic.com
2. "Sign up" karo (free)
3. Left menu → "API Keys"
4. "Create Key" pe click karo
5. Copy karo → App mein paste karo

> ⚠️ Free trial mein $5 ka credit milta hai — kaafi hai testing ke liye

---

## PART 5: Kuch Problem Aaye Toh

**"Module not found" error:**
Terminal mein likho: `pip install anthropic streamlit`

**App nahi chal rahi:**
Check karo `app.py` file sahi folder mein hai

**Streamlit deploy fail ho rahi:**
requirements.txt file check karo — sahi jagah honi chahiye

---

*Koi dikkat aaye toh seedha pooch!* 🙌
