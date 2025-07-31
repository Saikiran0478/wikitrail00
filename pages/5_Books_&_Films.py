import streamlit as st
import requests
from urllib.parse import quote_plus
from utils import render_footer

st.set_page_config(page_title="📚 Book Shelf", layout="wide")
st.title("📚 Explore Books Related to Your Topic")

query = st.session_state.get("selected_topic", "Artificial Intelligence")

def fetch_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={quote_plus(query)}"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        books = r.json().get("items", [])[:10]
        return [{
            "title": b["volumeInfo"].get("title", "No title"),
            "authors": b["volumeInfo"].get("authors", []),
            "desc": b["volumeInfo"].get("description", "No description."),
            "thumbnail": b["volumeInfo"].get("imageLinks", {}).get("thumbnail", ""),
            "preview": b["volumeInfo"].get("previewLink", "")
        } for b in books]
    except:
        return []

books = fetch_books(query)

if not books:
    st.warning("No books found for this topic.")
else:
    # 🔽 BOOKS STYLING + DISPLAY
    st.markdown("""
        <style>
        .carousel-container {
            display: flex;
            overflow-x: auto;
            gap: 20px;
            padding: 15px 5px;
        }
        .carousel-container::-webkit-scrollbar { height: 8px; }
        .carousel-container::-webkit-scrollbar-thumb { background: #ccc; border-radius: 10px; }

        .book-card {
            flex: 0 0 auto;
            width: 210px;
            background: #ffffff10;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .book-card:hover { transform: scale(1.04); }
        .book-card img { width: 100%; height: 250px; object-fit: cover; }

        .book-info { padding: 10px; font-size: 13px; }
        .book-info h4 { font-size: 15px; margin: 8px 0 4px 0; text-align: center; }
        .book-info .authors { text-align: center; font-size: 12px; color: #555; }

        .book-info .desc {
            max-height: 70px;
            overflow-y: auto;
            font-size: 12px;
            margin-top: 8px;
            color: #333;
        }

        .book-info .desc::-webkit-scrollbar { width: 4px; }
        .book-info .desc::-webkit-scrollbar-thumb { background: #aaa; border-radius: 6px; }

        .book-links {
            display: flex;
            justify-content: space-around;
            margin: 10px 0;
        }

        .book-links a {
            font-size: 12px;
            padding: 5px 10px;
            border-radius: 6px;
            color: white;
            text-decoration: none;
        }

        .google-link { background-color: #4285F4; }
        .amazon-link { background-color: #FF9900; }

        /* Movies Section */
        .imdb-section {
            margin-top: 40px;
            background: #fdfdfd;
            border-left: 6px solid #F5C518;
            padding: 16px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.07);
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .imdb-section img {
            height: 80px;
            border-radius: 8px;
        }

        .imdb-section .content {
            flex-grow: 1;
        }

        .imdb-section .imdb-link {
            background-color: #F5C518;
            color: black;
            padding: 8px 16px;
            font-weight: bold;
            border-radius: 8px;
            text-decoration: none;
            margin-top: 8px;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)

    # Render Books
    st.markdown('<div class="carousel-container">', unsafe_allow_html=True)
    for book in books:
        title = book['title']
        authors = ", ".join(book['authors']) if book['authors'] else "Unknown"
        desc = book['desc'][:300] + "..." if book['desc'] else "No description."
        img = book['thumbnail'] or "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
        google_link = book['preview']
        amazon_link = f"https://www.amazon.com/s?k={quote_plus(title)}"

        card = f"""
        <div class="book-card">
            <img src="{img}" alt="{title}">
            <div class="book-info">
                <h4>{title}</h4>
                <div class="authors"><em>{authors}</em></div>
                <div class="desc">{desc}</div>
                <div class="book-links">
                    <a href="{google_link}" target="_blank" class="google-link">Google</a>
                    <a href="{amazon_link}" target="_blank" class="amazon-link">Amazon</a>
                </div>
            </div>
        </div>
        """
        st.markdown(card, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("**Get Movies suggestions from IMDB**")

    # 🎬 IMDb Section
    imdb_url = f"https://www.imdb.com/find?q={quote_plus(query)}&s=tt"

    imdb_html = f"""
    <div class="imdb-section">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg" />
        <div class="content">
            <h4>🎬 Explore Movies Related to <em>{query}</em></h4>
            <a class="imdb-link" href="{imdb_url}" target="_blank">Search on IMDb</a>
        </div>
    </div>
    """
    st.markdown(imdb_html, unsafe_allow_html=True)

render_footer()