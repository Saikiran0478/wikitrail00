# utils.py
import requests
import streamlit as st
import re

# === OLLAMA: Local Chatbot ===
def query_chatbot(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",  # use your pulled Ollama model here
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "No response.")
    except Exception as e:
        return f"Ollama Error: {str(e)}"


def generate_advanced_info(summary):
    prompt = f"""
    You're an expert teacher. Expand this summary of a topic:

    Summary: {summary}

    Return in this format:
    - Key Subtopics
    - Definitions
    - Real-world Applications
    - Background
    """
    return query_chatbot(prompt)


def clean_bot_response(full_response, prompt):
    response = full_response.replace(prompt, "")
    cleanup_phrases = [
        "You are a movie expert.",
        "You are a Wikipedia assistant.",
        "You can say:",
        "User:",
        "Answer:",
        "Bot:",
        prompt
    ]
    for phrase in cleanup_phrases:
        response = response.replace(phrase, "")
    response = re.sub(r"\n+", "\n", response).strip()
    return response


def render_chatbot(topic="this topic"):
    if st.session_state.get("suppress_chatbot"):
        return

    with st.sidebar:
        st.markdown("## 🤖 WikiBot")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("Ask anything about this topic:", key="chat_input")
        if st.button("Send"):
            if user_input:
                prompt = f"You are a helpful assistant. The user is learning about '{topic}'. They ask: '{user_input}'"
                raw_response = query_chatbot(prompt)
                clean_response = clean_bot_response(raw_response, prompt)
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", clean_response))

        for role, message in reversed(st.session_state.chat_history):
            with st.chat_message(role):
                st.markdown(message)


def get_topic_emoji(topic: str) -> str:
    category_emoji_map = {
        "automotive": "🚗", "vehicles": "🚗", "transport": "🚌",
        "aircraft": "✈", "space": "🚀", "astronomy": "🌌",
        "astronaut": "🧑‍🚀", "robotics": "🤖", "robot": "🤖",
        "ai": "🧠", "artificial intelligence": "🧠", "computer": "💻",
        "software": "💻", "hardware": "🖥", "biology": "🧬",
        "genetics": "🧬", "chemistry": "⚗", "physics": "🧲",
        "mathematics": "📐", "music": "🎵", "instrument": "🎻",
        "film": "🎬", "movie": "🎥", "finance": "💰",
        "banking": "🏦", "india": "🇮🇳", "country": "🌍",
        "language": "🗣", "literature": "📚", "writer": "✍",
        "history": "📜", "military": "🪖", "politics": "🏛",
        "education": "🎓", "school": "🏫", "university": "🎓",
        "engineering": "🛠"
    }

    try:
        topic_encoded = topic.replace(" ", "_")
        url = f"https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "prop": "categories",
            "format": "json",
            "titles": topic_encoded
        }

        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        categories = []
        for page in pages.values():
            categories = [cat["title"].lower() for cat in page.get("categories", [])]

        for cat in categories:
            for keyword, emoji in category_emoji_map.items():
                if keyword in cat:
                    return emoji
    except Exception as e:
        print("⚠ Emoji fetch failed:", e)

    return "•"


INDICTRANS_API = "https://api-inference.huggingface.co/models/ai4bharat/indictrans2-en-indic"
HF_TOKEN = st.secrets.get("HF_TOKEN")

lang_code_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn"
}

def t(text, target_lang=None):
    lang = target_lang or st.session_state.get("language", "English")
    if lang == "English":
        return text

    tgt_lang_code = lang_code_map.get(lang)
    if not tgt_lang_code:
        return text

    payload = {
        "inputs": text,
        "parameters": {
            "src_lang": "en",
            "tgt_lang": tgt_lang_code
        }
    }

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    try:
        response = requests.post(INDICTRANS_API, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()[0]["translation_text"]
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text


def render_footer():
    st.markdown("""---""")
    st.markdown("### 🌐 Connect with Us")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <a href="mailto:putha.hemanth@gmail.com">
                <img src="https://moein.video/wp-content/uploads/2022/12/Gmail-Logo-GIF-Gmail-Icon-GIF-Royalty-Free-Animated-Icon-GIF-1080px-after-effects-project.gif" width="80" />
            </a>
            <br/>
            <a href="mailto:putha.hemanth@gmail.com" style="color: #ff4d4d;">Email</a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://instagram.com/_heman.th_" target="_blank">
                <img src="https://miro.medium.com/v2/resize:fit:1400/1*PPztoHHx7GPXCwTUHMmr4w.gif" width="150" />
            </a>
            <br/>
            <a href="https://instagram.com/_heman.th_" target="_blank" style="color: #e75480;">Instagram</a>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://twitter.com/yourproject" target="_blank">
                <img src="https://cdn.dribbble.com/userupload/9051959/file/original-006a32a7d1299ce2651e2835f852d90b.gif" width="80" />
            </a>
            <br/>
            <a href="https://twitter.com/yourproject" target="_blank" style="color: #66ccff;">Twitter</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""---""")

    with st.expander("👥 Team Members"):
        st.markdown("""
        - [*Hemanth Kumar Putha*](mailto:putha.hemanth@gmail.com)  
        - [*Mangali Saikiran*](mailto:mangalisaikiran23@ifheindia.org)  
        - [*Guduri Abhishek*](mailto:guduriabhishek23@ifheindia.org)  
        - [*Rachamalla Himavantha Reddy*](mailto:rhimavanthareddy23@ifheindia.org)  
        """, unsafe_allow_html=True)

    st.markdown("""
        <p style="text-align:center; font-size:0.8rem; color:gray; margin-top: 2rem;">
            © 2025 YourProject. Built with ❤ by the team. No copyright. Feel free to use with credit.
        </p>
    """, unsafe_allow_html=True)