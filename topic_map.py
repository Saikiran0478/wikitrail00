import re
import json
import requests
from bs4 import BeautifulSoup

import re
import requests

def generate_topic_timeline(topic):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": topic,
        "format": "json",
        "prop": "sections"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        sections = data["parse"]["sections"]
        
        # Find 'History' or similar section
        history_section_index = None
        for section in sections:
            if "history" in section["line"].lower():
                history_section_index = section["index"]
                break

        if history_section_index is None:
            return [{"start_date": {"year": 2000}, "text": {"headline": "No Timeline", "text": "No historical data found."}}]

        # Now get content of the History section
        content_params = {
            "action": "parse",
            "page": topic,
            "format": "json",
            "prop": "text",
            "section": history_section_index
        }

        content_response = requests.get(url, params=content_params)
        content_response.raise_for_status()
        html = content_response.json()["parse"]["text"]["*"]

        import bs4
        soup = bs4.BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        # Extract year-based sentences
        sentences = text.split(". ")
        timeline = []

        for sentence in sentences:
            years = re.findall(r"(1[0-9]{3}|20[0-9]{2})", sentence)
            if years:
                year = int(years[0])
                timeline.append({
                    "start_date": {"year": year},
                    "text": {
                        "headline": f"{year}",
                        "text": sentence.strip()
                    }
                })

        if not timeline:
            timeline.append({
                "start_date": {"year": 2000},
                "text": {"headline": "No Events Found", "text": "No clear events could be parsed from Wikipedia."}
            })

        # Sort by year
        timeline.sort(key=lambda x: x["start_date"]["year"])
        return timeline

    except Exception as e:
        return [{"start_date": {"year": 2000}, "text": {"headline": "Error", "text": str(e)}}]
