# 💬 SmartChat AI  

**SmartChat AI** is an intelligent conversational web app that provides accurate, real-time answers to user queries on any topic — powered by **Hugging Face Transformers** and **Streamlit**.  
The app dynamically retrieves and processes relevant content from the web to generate **context-aware, fact-based responses** with a smooth, chat-style interface.

---

## 🚀 Key Features

- 🧠 **Transformer-Based QA Model** — Uses a fine-tuned model (`deepset/roberta-base-squad2`) from Hugging Face for context-aware question answering.  
- 🌐 **Dynamic Knowledge Retrieval** — Automatically scrapes relevant text from trusted sources like **Wikipedia** using BeautifulSoup and Requests.  
- 💬 **Chat-Style Interface** — Interactive, user-friendly Streamlit chat UI that maintains smooth conversation flow.  
- 🧩 **Context Chunking** — Handles large text by splitting it into smaller sections and finding the best context for each question.  
- ⚡ **Performance Optimized** — Uses caching and efficient token handling for faster responses.  
- 🚨 **Graceful Fallbacks** — Returns “Sorry, I am unaware of this topic.” when no relevant content is found.  

---

## 🛠️ Tech Stack

| Component | Description |
|------------|-------------|
| **Frontend/UI** | Streamlit |
| **Model** | `deepset/roberta-base-squad2` (Hugging Face Transformers) |
| **Web Scraping** | BeautifulSoup4 + Requests |
| **Language** | Python 3.x |
| **Deployment** | Streamlit Community Cloud / Localhost |

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
