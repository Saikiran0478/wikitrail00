import streamlit as st
import random
import requests
from utils import render_footer

st.set_page_config(page_title="🧠 Quiz & Advanced", layout="wide")

if "selected_topic" not in st.session_state:
    st.warning("⚠️ Please select a topic from the homepage.")
    st.stop()

topic = st.session_state["selected_topic"]
st.title(f"🧠 Quiz: {topic}")

difficulty = st.radio("🧪 Choose Difficulty:", ["Easy", "Medium", "Hard"], horizontal=True)
difficulty_map = {"Easy": 3, "Medium": 5, "Hard": 7}
num_questions = difficulty_map[difficulty]

# 🧠 Fetch Wikipedia Summary
@st.cache_data(show_spinner=False)
def fetch_summary(topic):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json().get("extract", "")
    except:
        return ""

summary_text = fetch_summary(topic)

# 🧩 Generate MCQs
def generate_mcqs(text, num_qs, difficulty_level):
    sentences = [s.strip() for s in text.split('.') if len(s.split()) > 6]
    if not sentences:
        return []

    if difficulty_level == "Easy":
        selected_sentences = sentences[:num_qs]
    elif difficulty_level == "Medium":
        selected_sentences = sentences[:num_qs * 2][::2]
    else:  # Hard
        selected_sentences = random.sample(sentences, min(num_qs, len(sentences)))

    questions = []

    for i, sentence in enumerate(selected_sentences[:num_qs]):
        words = [w.strip(",.") for w in sentence.split()]
        long_words = [w for w in words if len(w) > 4]
        short_words = [w for w in words if 3 < len(w) <= 5]

        # Easy = shorter word, Medium = longest, Hard = random
        if difficulty_level == "Easy" and short_words:
            keyword = random.choice(short_words)
        elif difficulty_level == "Hard" and long_words:
            keyword = random.choice(long_words)
        else:
            keyword = max(words, key=len)

        if len(keyword) < 3 or sentence.count(keyword) > 1:
            continue  # skip over-repeated

        correct = keyword
        distractors = list({w for w in words if w != keyword and len(w) > 4})
        wrong = random.sample(distractors, min(3, len(distractors))) if distractors else ["None", "N/A", "Skip"]
        options = wrong + [correct]
        random.shuffle(options)

        q = {
            "id": f"q{i}",
            "question": sentence.replace(correct, "_____"),
            "options": options,
            "answer": correct
        }
        questions.append(q)

    return questions

quiz_key = f"quiz_{topic}_{difficulty}"
if quiz_key not in st.session_state:
    st.session_state[quiz_key] = generate_mcqs(summary_text, num_questions, difficulty)

questions = st.session_state[quiz_key]
user_answers = {}

if not questions:
    st.error("⚠️ Could not generate questions. Try another topic.")
    st.stop()

# 🎯 Quiz Form
with st.form("quiz_form"):
    for q in questions:
        user_answers[q["id"]] = st.radio(f"**{q['question']}**", options=q["options"], key=f"{q['id']}_{difficulty}")
    submitted = st.form_submit_button("Submit Answers")

if submitted:
    score = 0
    for q in questions:
        selected = user_answers[q["id"]]
        if selected == q["answer"]:
            st.success(f"✅ Correct: {q['answer']}")
            score += 1
        else:
            st.error(f"❌ Incorrect. You chose: {selected} | Correct: {q['answer']}")

    st.markdown(f"### 🎯 Final Score: `{score} / {len(questions)}`")

    if score == len(questions):
        st.balloons()

# 🚀 Advanced Exploration
st.markdown("---")
st.markdown("### 🔍 Want to dive deeper?")
if st.button("Go to Advanced Exploration ➡️"):
    st.switch_page("pages/2_Concept_Mapping.py")

render_footer()
