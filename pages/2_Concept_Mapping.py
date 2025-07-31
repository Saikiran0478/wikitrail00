import streamlit as st
from pyvis.network import Network
import tempfile
import os
import networkx as nx
import streamlit.components.v1 as components
from topic_map import generate_topic_timeline
import streamlit_timeline
import json
import wikipediaapi
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from utils import render_footer

# ----------------------------- Validate Session -----------------------------
if "selected_topic" not in st.session_state:
    st.warning("⚠ No topic selected. Please go to the homepage and enter a topic.")
    st.stop()

root_topic = st.session_state["selected_topic"]
language = st.session_state.get("language", "English")

st.markdown(f"### 🧠 Concept Mapping for: *{root_topic}*")
st.caption(f"🌐 Language: {language}")
st.markdown("---")

# ----------------------------- Wikipedia Summary ---------------------------
def get_wikipedia_summary(topic):
    wiki = wikipediaapi.Wikipedia(language='en', user_agent='wikiverse-bot/1.0')
    page = wiki.page(topic)
    return page.summary if page.exists() else "No summary found."

summary = get_wikipedia_summary(root_topic)
st.subheader("🔎 Quick Summary")
st.info(summary)

# ----------------------------- Keyword Extraction ---------------------------
tokenizer = RegexpTokenizer(r'\w+')

def extract_keywords(text):
    words = tokenizer.tokenize(text)
    stop_words = set(stopwords.words('english'))
    keywords = [w.lower() for w in words if w.lower() not in stop_words]
    return list(set(keywords))

keywords = extract_keywords(summary)

# ----------------------------- Concept Map Graph ----------------------------
st.subheader("🧠 Concept Graph")

graph = nx.Graph()
graph.add_node(root_topic, size=30, title=root_topic)

for kw in keywords:
    graph.add_node(kw, size=10, title=kw)
    graph.add_edge(root_topic, kw)

net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")
net.from_nx(graph)

with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
    net.save_graph(tmp_file.name)
    html_path = tmp_file.name

with open(html_path, 'r', encoding='utf-8') as f:
    graph_html = f.read()

components.html(graph_html, height=550)

# ----------------------------- Timeline -------------------------------------
st.subheader("📅 Timeline")

timeline_data = generate_topic_timeline(root_topic)

if timeline_data:
    streamlit_timeline.timeline(json.dumps({"events": timeline_data}), height=600)
else:
    st.info("❌ No timeline data could be extracted for this topic.")

# ----------------------------- Footer ---------------------------------------
render_footer()