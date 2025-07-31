import streamlit as st
import requests
from urllib.parse import quote_plus
from utils import render_footer

st.set_page_config(page_title="💼 Careers & Jobs", layout="wide")
st.title("💼 Career Opportunities")

# ✅ Topic check
if "selected_topic" not in st.session_state:
    st.warning("Please go back and select a topic.")
    st.stop()

topic = st.session_state["selected_topic"]
st.success(f"Showing careers for: **{topic}**")

# ✅ Wikipedia Extractor (Summary + Content)
@st.cache_data(show_spinner=False)
def fetch_career_related_content(query):
    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}"
    content_url = f"https://en.wikipedia.org/api/rest_v1/page/mobile-sections/{quote_plus(query)}"

    summary, content = "", ""

    try:
        s_resp = requests.get(summary_url, timeout=4)
        if s_resp.status_code == 200:
            summary = s_resp.json().get("extract", "")
    except:
        pass

    try:
        c_resp = requests.get(content_url, timeout=6)
        if c_resp.status_code == 200:
            all_sections = c_resp.json().get("sections", [])
            for section in all_sections:
                if "career" in section.get("line", "").lower() or "application" in section.get("line", "").lower():
                    content += section.get("text", "")
    except:
        pass

    return summary, content

# ✅ Filter relevant lines
def extract_career_lines(text):
    lines = text.replace('\n', '. ').split('. ')
    career_lines = [line.strip() for line in lines if any(word in line.lower() for word in ["career", "job", "employment", "industry", "work", "application", "field"])]
    return list(set(career_lines))

# ✅ Get info
summary_text, content_text = fetch_career_related_content(topic)
career_lines = extract_career_lines(summary_text + " " + content_text)

# ✅ Display
st.markdown("### 📘 Overview")
if summary_text:
    st.info(summary_text)
else:
    st.warning("No summary available.")

st.markdown("### 💼 Career/Job Insights")

if career_lines:
    for line in career_lines:
        st.markdown(f"- 🔹 {line}")
else:
    fallback = {
        "electronics": [
            "Electronics Engineer", "Embedded Systems Developer", "PCB Designer",
            "Semiconductor Process Engineer", "VLSI Design Engineer", "IoT Developer",
            "Control Systems Engineer", "Analog Design Engineer"
        ],
        "artificial intelligence": [
            "AI Researcher", "Machine Learning Scientist", "Data Scientist",
            "NLP Engineer", "Computer Vision Engineer", "Ethics AI Consultant"
        ],
        "robotics": [
            "Robotics Engineer", "Automation Specialist", "Mechatronics Engineer",
            "Robot Software Developer", "Human-Robot Interaction Designer"
        ],
        "computer science": [
            "Software Developer", "System Architect", "Cybersecurity Analyst",
            "Cloud Engineer", "UI/UX Designer", "DevOps Engineer"
        ],
        "space": [
            "Astrophysicist", "Satellite Engineer", "Mission Control Analyst",
            "Orbital Analyst", "Payload Specialist"
        ],
        "biology": [
            "Biotechnologist", "Geneticist", "Biomedical Engineer",
            "Molecular Biologist", "Neuroscience Researcher"
        ],
        "energy": [
            "Power Systems Engineer", "Energy Consultant", "Renewable Energy Engineer",
            "Smart Grid Analyst"
        ],
        "education": [
            "Instructional Designer", "Curriculum Developer", "Online Learning Specialist",
            "Academic Researcher", "Educational Technologist"
        ],
        "climate": [
            "Climate Scientist", "Environmental Engineer", "Sustainability Consultant",
            "Carbon Analyst", "Disaster Risk Planner"
        ],
        "language": [
            "Linguist", "Language Technologist", "Translator", "Speech Recognition Engineer",
            "Language Corpus Curator"
        ],
    }

    found = False
    topic_lower = topic.lower()

    for key, careers in fallback.items():
        if key in topic_lower:
            st.info("⚠️ Couldn't find career info in Wikipedia directly. Showing fallback results:")
            for job in careers:
                st.markdown(f"- 🔹 {job}")
            found = True
            break

    if not found:
        st.warning("⚠️ No career data found for this topic.")
        st.markdown("Try searching a more specific topic, or use keywords like *AI*, *Robotics*, *Electronics*, etc.")

# ✅ Explore Jobs
st.markdown("---")
st.markdown("### 🔗 External Job Portals")
job_links = {
    "💼 LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={topic}",
    "🧰 Indeed": f"https://in.indeed.com/jobs?q={topic}",
    "📈 Naukri": f"https://www.naukri.com/{topic}-jobs",
    "🎓 Internshala (Internships)": f"https://internshala.com/internships/keywords-{topic}"
}

# Display links in markdown
for platform, url in job_links.items():
    st.markdown(f"- [{platform}]({url})")

render_footer()
