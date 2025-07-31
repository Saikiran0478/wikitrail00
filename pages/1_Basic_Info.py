# pages/1_Basic_Info.py

import streamlit as st
import requests
from utils import render_chatbot, generate_advanced_info, get_topic_emoji, render_footer

st.set_page_config(
    page_title="Basic Info - WikiVerse Pro",
    page_icon="📖",
    layout="wide",
)

# 🔽 Background GIF using custom CSS
# 🔽 Background GIF with better shaded overlay for readability
# 🔽 Background GIF with shaded overlay and content wrapper
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://pcyti.izt.uam.mx/wp-content/uploads/tier.gif");
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


# ✅ Get topic first
if "selected_topic" not in st.session_state:
    st.warning("Please go back to the homepage and enter a topic.")
    st.stop()

topic = st.session_state["selected_topic"]
language = st.session_state.get("language", "English")

# ✅ Now pass it to the chatbot
render_chatbot(topic)

st.markdown('<div class="custom-container">', unsafe_allow_html=True)


st.title(f"📖 Basic Info: {topic}")
st.caption(f"🔤 Language: {language}")

# --- Wikipedia API Call ---
def get_summary(topic, lang="en"):
    try:
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("title", topic), data.get("extract", "No summary available."), data.get("thumbnail", {}).get("source", None)
    except Exception as e:
        return topic, "Error retrieving summary.", None


# Language code mapping (for Wikipedia API)
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn"
}
wiki_lang = lang_map.get(language, "en")

title, summary, image = get_summary(topic, lang=wiki_lang)

# --- Display Summary ---
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader(title)
    st.write(summary)

with col2:
    if image:
        st.image(image, width=300)
    else:
        st.info("No image available.")

# Navigation option to next page
if st.button("Next ➡️ Concept Mapping"):
    st.switch_page("pages/2_Concept_Mapping.py")

# --- Expandable: Show Advanced Information from Wikipedia Sections ---
# --- Advanced Info from Wikipedia Sections (No nested expanders) ---
st.markdown("### 📘 Advanced Information (from Wikipedia Sections)")

def get_wikipedia_sections(topic, lang="en"):
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": topic,
        "format": "json",
        "prop": "sections"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        sections = response.json().get("parse", {}).get("sections", [])
        return [s for s in sections if int(s["toclevel"]) <= 2]
    except Exception as e:
        return []

def get_section_content(topic, section_index, lang="en"):
    import bs4, re

    # --- Emoji map for topic categories ---
    emoji_map = {
        "dinosaurs": "🦕",
        "space": "🚀",
        "astronomy": "🌌",
        "robot": "🤖",
        "robotics": "🤖",
        "computer": "💻",
        "ai": "🧠",
        "india": "🇮🇳",
        "physics": "🧲",
        "chemistry": "⚗️",
        "biology": "🧬",
        "history": "📜",
        "math": "📐",
        "music": "🎵",
        "climate": "🌍",
        "economy": "💰",
        "literature": "📚",
        "language": "🗣️"
    }

    # --- Choose emoji based on topic ---
    bullet = get_topic_emoji(topic)


    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": topic,
        "format": "json",
        "prop": "text",
        "section": section_index
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        html = response.json()["parse"]["text"]["*"]
        soup = bs4.BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        # --- Clean up junk ---
        text = re.sub(r"\[\d+\]", "", text)
        text = re.sub(r"\^ Cite error.*", "", text)
        text = re.sub(r"\n{2,}", "\n", text)
        text = re.sub(r"\n\s+", "\n", text)
        text = text.strip()

        # --- Break long lines into bullet points ---
        lines = text.split("\n")
        cleaned_lines = []

        important_terms = re.compile(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*|\d{4}|[A-Z]{2,})\b")

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if len(line) > 250:
                subpoints = re.split(r'(?<=[.!?])\s+(?=[A-Z])', line)
                for sp in subpoints:
                    if len(sp.strip()) < 3:
                        continue
                    highlighted = important_terms.sub(r"**\1**", sp.strip())
                    cleaned_lines.append(f"{bullet} {highlighted}")
            else:
                highlighted = important_terms.sub(r"**\1**", line)
                cleaned_lines.append(f"{bullet} {highlighted}")

        # Limit number of points
        formatted = "\n\n".join(cleaned_lines[:15])
        return formatted + "\n\n_ℹ️ Section summarized for clarity._"

    except Exception as e:
        return "❌ Error loading this section."

sections = get_wikipedia_sections(topic, wiki_lang)

if sections:
    for section in sections[:5]:  # Show only first 5 sections to keep it light
        with st.expander(f"🔹 {section['line']}"):
            content = get_section_content(topic, section["index"], wiki_lang)
            st.markdown(content)
else:
    st.info("No detailed sections found for this topic.")

st.markdown('</div>', unsafe_allow_html=True)


# At end of your page file
render_footer()
