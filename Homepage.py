# app.py
import streamlit as st
from utils import render_chatbot, t
import requests

st.set_page_config(
    page_title="WikiVerse Pro",
    page_icon="🌐",
    layout="wide",
)

render_chatbot()  # Sidebar chatbot

#change0
st.title(t("🌐 WikiVerse Pro"))
st.markdown(f"#### {t('Explore. Learn. Connect.')}")
language = st.selectbox(t("Choose language for results"), ["English", "Hindi", "Telugu", "Tamil", "Kannada"])
topic = st.text_input(t("🔍 Search Wikipedia Topic"), placeholder=t("e.g., Quantum Computing"))


# Optional: voice input (in future)
st.caption("🎙 Voice search and Indic typing support coming soon!")

if st.button("Explore"):
    if topic:
        # Redirect to first page (you will handle topic routing via session_state)
        st.session_state["selected_topic"] = topic
        st.session_state["language"] = language
        st.switch_page("pages/1_Basic_Info.py")  # Streamlit 1.25+ feature
    else:
        st.warning("Please enter a topic to explore.")

def get_translated_topic_title(topic, lang="en"):
    try:
        search_url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "search": topic,
            "limit": 1,
            "namespace": 0,
            "format": "json"
        }
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data[1][0] if data[1] else topic
    except:
        return topic