import streamlit as st
from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import re

#--------------------------------------------------------------
# Page Configuration
st.set_page_config(page_title="SmartChat AI", page_icon="💬", layout="centered")

#--------------------------------------------------------------
# Styling (clean chat-style UI)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-bubble {
        border-radius: 15px;
        padding: 12px 18px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #0078ff;
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
    .bot-bubble {
        background-color: #262730;
        color: #ffffff;
        align-self: flex-start;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

#--------------------------------------------------------------
# Function to fetch and clean topic context
@st.cache_data(show_spinner=False)
def fetch_topic_context(topic):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}", headers=headers, timeout=10)

        # Handle failed responses
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from multiple HTML tags
        elements = soup.find_all(['p', 'li', 'div', 'span'])
        text = ' '.join([el.get_text(separator=' ', strip=True) for el in elements])

        # Clean up messy content
        text = re.sub(r'\[[0-9]+\]', '', text)  # remove citations like [1]
        text = re.sub(r'\s+', ' ', text)        # remove multiple spaces
        text = re.sub(r'\([^)]*\)', '', text)   # remove parentheses content (optional)
        text = text.strip()

        # If nothing meaningful is fetched
        if len(text) < 3000:
            return None

        # Cap maximum context for performance
        return text[:25000]

    except Exception:
        return None

#--------------------------------------------------------------
# Function to split long text into smaller chunks
def split_text(text, max_chunk_length=15000):
    sentences = text.split('. ')
    chunks, current_chunk = [], ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

#--------------------------------------------------------------
# Load QA Model
@st.cache_resource
def load_model():
    return pipeline(
        "question-answering",
        model="valhalla/longformer-base-4096-finetuned-squadv1",
        tokenizer="valhalla/longformer-base-4096-finetuned-squadv1"
    )

qa_pipeline = load_model()

#--------------------------------------------------------------
# Function for long context QA
def long_context_qa(question, context):
    try:
        chunks = split_text(context)
        all_answers = []
        for chunk in chunks:
            result = qa_pipeline(question=question, context=chunk)
            all_answers.append(result)
        best = max(all_answers, key=lambda x: x["score"])
        return best["answer"]
    except Exception:
        return "Sorry, I’m unaware of this topic."

#--------------------------------------------------------------
# Chatbot Interface
st.title("💬 SmartChat AI")
st.caption("Your intelligent assistant — ask anything!")

# Sidebar Input
topic = st.text_input("Enter a topic to discuss:", placeholder="e.g. Artificial Intelligence")

if topic:
    with st.spinner("Gathering knowledge..."):
        context = fetch_topic_context(topic)

    if not context:
        st.error("Sorry, I’m unaware of this topic. Try another one!")
    else:
        st.success(f"Start chatting below 👇")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.chat_input(f"Ask me anything about {topic}...")

        if user_input:
            with st.spinner("Thinking..."):
                answer = long_context_qa(user_input, context)
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", answer))

        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f'<div class="chat-bubble user-bubble">{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble bot-bubble">{msg}</div>', unsafe_allow_html=True)
else:
    st.info("Please enter a topic above to start chatting.")
