import streamlit as st
import requests
from urllib.parse import quote_plus
from utils import render_footer, render_chatbot

st.set_page_config(page_title="💬 Forums & Discussions", layout="wide")
st.title("💬 Forums & Community Discussions")

if "selected_topic" not in st.session_state:
    st.warning("⚠️ No topic selected. Please go to the homepage and enter a topic.")
    st.stop()

topic = st.session_state["selected_topic"]
encoded = quote_plus(topic)

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://www.icegif.com/wp-content/uploads/2023/08/icegif-769.gif");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .block-container {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 17rem;
        border-radius: 10px;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: white !important;
    }
    input, .stSelectbox div, .stSelectbox input, .stTextInput input {
        color: black !important;
        background-color: white !important;
    }
    </style>
""", unsafe_allow_html=True)


st.success(f"🔍 Community discussions and resources for: **{topic}**")
st.markdown("---")

# 🎯 General search engines and Q&A platforms
platforms = {
    "Reddit": {
        "url": f"https://www.reddit.com/search/?q={encoded}",
        "icon": "https://upload.wikimedia.org/wikipedia/en/thumb/1/1f/Reddit_logo_2023.svg/768px-Reddit_logo_2023.svg.png"
    },
    "YouTube": {
        "url": f"https://www.youtube.com/results?search_query={encoded}+explanation+discussion",
        "icon": "https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"
    },
    "Quora": {
        "url": f"https://www.quora.com/search?q={encoded}",
        "icon": "https://download.logo.wine/logo/Quora/Quora-Logo.wine.png"
    },
    "Amazon": {
        "url": f"https://www.amazon.com/s?k={encoded}",
        "icon": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg"
    },
    "Wikipedia Talk": {
        "url": f"https://en.wikipedia.org/wiki/Talk:{encoded.replace(' ', '_')}",
        "icon": "https://upload.wikimedia.org/wikipedia/commons/8/80/Wikipedia-logo-v2.svg"
    },
    "Google Forums": {
        "url": f"https://groups.google.com/g/{encoded}",
        "icon": "https://br.atsit.in/wp-content/uploads/2021/02/a-atualizacao-dos-grupos-do-google-altera-a-maneira-como-os-nomes-dos-membros-sao-exibidos-e-os-proprietarios-desejam-uma-opcao-para-editar-nomes-ou-uma-reversao.jpg"
    },
}

# 🖼️ Display platform cards
cols = st.columns(3)
for i, (name, data) in enumerate(platforms.items()):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="text-align: center;">
            <a href="{data['url']}" target="_blank">
                <img src="{data['icon']}" width="80" />
                <div style="margin-top: 0.5rem; font-weight: bold; color: white;">{name}</div>
            </a>
        </div>
        """, unsafe_allow_html=True)

render_footer()

# 🔁 Navigation Buttons
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("⬅️ Previous"):
        st.switch_page("pages/2_Concept_Mapping.py")

with col3:
    if st.button("Next ➡️"):
        st.switch_page("pages/4_Give_Review_Here.py")

with col2:
    if st.button("🔁 New Search"):
        for key in ["selected_topic"]:
            st.session_state.pop(key, None)
        st.switch_page("Home.py")
