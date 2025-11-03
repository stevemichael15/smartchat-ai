import streamlit as st
from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import re

#--------------------------------------------------------------
# Page Configuration
st.set_page_config(page_title="SmartChat AI", page_icon="💬", layout="centered")

#--------------------------------------------------------------
# Styling
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

        if response.status_code != 200:
            return None, None

        soup = BeautifulSoup(response.text, 'html.parser')

        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return None, None

        paragraphs = content_div.find_all('p')
        all_text = ' '.join([p.get_text(separator=' ', strip=True) for p in paragraphs])

        # Clean text
        all_text = re.sub(r'\[[0-9]+\]', '', all_text)
        all_text = re.sub(r'\s+', ' ', all_text)
        all_text = re.sub(r'\([^)]*\)', '', all_text)
        all_text = all_text.strip()

        # ✅ Extract the first meaningful paragraph for "Did You Know"
        intro_para = ""
        for p in paragraphs:
            clean_p = p.get_text(strip=True)
            if len(clean_p) > 50:
                intro_para = clean_p
                break

        # ✅ Make it short & concise (first 2–3 sentences only)
        if intro_para:
            sentences = re.split(r'(?<=[.!?]) +', intro_para)
            intro_para = ' '.join(sentences[:1]).strip()

        if len(all_text) < 1000:
            return None, None

        return all_text[:25000], intro_para

    except Exception:
        return None, None

#--------------------------------------------------------------
# Function to split long text into smaller chunks
def split_text(text, max_chunk_length=16000):
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
# Load Models
@st.cache_resource
def load_qa_model():
    return pipeline(
        "question-answering",
        model="valhalla/longformer-base-4096-finetuned-squadv1",
        tokenizer="valhalla/longformer-base-4096-finetuned-squadv1"
    )

qa_pipeline = load_qa_model()

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
# SmartChat Interface
st.title("💬 SmartChat AI")
st.caption("Your intelligent assistant — ask anything!")

# Sidebar Input
topic = st.text_input("Enter a topic to discuss:", placeholder="e.g. Artificial Intelligence")

if st.button("🔄 Change Topic"):
    st.session_state.clear()
    st.rerun()

if topic:
    with st.spinner("Gathering knowledge..."):
        context, intro = fetch_topic_context(topic)

    if not context:
        st.error("Sorry, I’m unaware of this topic. Try another one!")
    else:
        # ✅ Short, clean "Did You Know" section
        st.subheader("💡 Did You Know?")
        if intro:
            st.markdown(f"✨ **{intro}**")
        else:
            st.info("Couldn't find a short intro for this topic.")

        st.success("Start chatting below 👇")

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
