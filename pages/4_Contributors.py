
# ✅ Ensure a topic is selected
import streamlit as st
import requests
import json
from urllib.parse import quote_plus
from utils import render_footer
from streamlit_extras.stylable_container import stylable_container


st.set_page_config(page_title="👥 Contributors", layout="wide")
st.title("👥 Notable Contributors")

if "selected_topic" not in st.session_state:
    st.warning("⚠️ No topic selected. Please go to the homepage and enter a topic.")
    st.stop()

topic = st.session_state["selected_topic"]
encoded = quote_plus(topic)

st.markdown(f"Showing key contributors related to **{topic}**.")

# ✅ Function: Ask GPT to get contributors
def get_contributor_names(topic):
    try:
        prompt = f"List 5 people who made major contributions to the topic '{topic}', such as scientists, inventors, researchers, or pioneers. Respond with just a plain list of names."
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-large",
            headers={"Authorization": f"Bearer YOUR_HUGGINGFACE_API_KEY"},
            json={"inputs": prompt},
            timeout=10
        )
        names = response.json()[0]["generated_text"]
        return [name.strip() for name in names.split("\n") if name.strip()]
    except Exception as e:
        return []

# ✅ Function: Get Wikipedia info of a person
def get_person_info(name, lang="en"):
    try:
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote_plus(name)}"
        r = requests.get(url).json()
        return {
            "title": r.get("title", name),
            "summary": r.get("extract", "No description available."),
            "image": r.get("thumbnail", {}).get("source", None)
        }
    except:
        return {"title": name, "summary": "No description available.", "image": None}

# ✅ Contributors generated via GPT/HF
contributor_names = get_contributor_names(topic)

if not contributor_names:
    st.info("No contributors found.")
else:
    st.markdown("---")
    for name in contributor_names:
        info = get_person_info(name)
        with stylable_container(f"card-{name}", css_styles="""
            border: 1px solid #ddd;
            padding: 1rem;
            border-radius: 12px;
            transition: 0.3s ease;
            background: #f9f9f9;
        """):
            cols = st.columns([1, 4, 1])
            with cols[0]:
                if info["image"]:
                    st.image(info["image"], width=100)
                else:
                    st.image("https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg", width=100)
            with cols[1]:
                st.markdown(f"### {info['title']}")
                st.markdown(info["summary"])
            with cols[2]:
                if st.button(f"🔍 Explore {info['title']}", key=name):
                    st.session_state["selected_topic"] = info["title"]
                    st.switch_page("pages/Homepage.py")  # ✅ Fix this path as per your homepage

# Footer and nav
render_footer()

col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️ Previous"):
        st.switch_page("pages/3_Forums.py")
with col3:
    if st.button("New Search"):
        st.session_state.pop("selected_topic", None)
        st.switch_page("pages/0_Home.py")  # ✅ Adjust path to your homepage


st.markdown("---")
render_footer()

# Navigation buttons
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️ Previous"):
        st.switch_page("pages/3_Forums.py")
with col3:
    if st.button("New Search"):
        st.session_state.pop("selected_topic", None)
        st.switch_page("Homepage.py")
