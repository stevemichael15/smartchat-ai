# 💬 SmartChat AI

**SmartChat AI** is a conversational web app that answers your questions intelligently on any topic you choose — just like ChatGPT.  
Built with **Streamlit** and **Hugging Face Transformers**, it scrapes and processes relevant knowledge dynamically, giving you contextual, accurate responses in real-time.

---

## 🚀 Features

- 🤖 **AI-Powered Responses** — Uses a transformer-based QA model (`longformer-base-4096`) fine-tuned on SQuAD for context-aware answers.  
- 🌐 **Automatic Knowledge Retrieval** — Fetches relevant, up-to-date content from trusted sources like Wikipedia.  
- 💡 **Interactive Chat Interface** — A sleek, modern chat UI built with Streamlit, optimized for readability and engagement.  
- ⚡ **Efficient Long Context Handling** — Automatically splits long content into smaller chunks and analyzes them intelligently.  
- 🧠 **Fallback Handling** — If relevant content isn’t found, the bot gracefully responds with “Sorry, I am unaware of this topic.”

---

## 🛠️ Tech Stack

| Component | Description |
|------------|-------------|
| **Frontend/UI** | Streamlit |
| **Model** | Longformer (`valhalla/longformer-base-4096-finetuned-squadv1`) |
| **Scraping** | BeautifulSoup + Requests |
| **Language** | Python 3.x |
| **Deployment** | Streamlit Community Cloud / Lightning AI |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/stevemichael15/smartchat-ai.git
cd smartchat-ai
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app
```bash
streamlit run main.py
```

### 4️⃣ Open in browser
```bash
(http://localhost:8501)
```
