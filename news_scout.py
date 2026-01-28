import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- CONFIGURATION ---
API_KEY = "pub_b64319539b4a4e55a4503c9fec422368"
STRESS_KEYWORDS = ["exam", "concern", "kill", "dead", "death", "illegal", "harm", "deadline", "accident", "police", "fire", "tuition", "crisis", "warning", "breaking news"]

# --- 1. THE UTILITIES ---

def get_article_lead(url):
    """Visits the article link and grabs the first 3 substantial paragraphs."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')
        content_blocks = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 80: 
                content_blocks.append(text)
            if len(content_blocks) == 3:
                break
        
        if content_blocks:
            return "\n\n".join(content_blocks)
            
    except:
        return "Lead content unavailable."
    return "No substantial content found."

def scan_for_stress(text):
    points = 0
    for word in STRESS_KEYWORDS:
        if word in text.lower():
            points += 15
    return points

# --- 2. THE ENGINES ---

def pull_local_news():
    sources = {
        "The Collegian": {"url": "https://www.thecollegianur.com/", "tag": "h3", "class": "headline"},
        "Richmond Times-Dispatch": {"url": "https://richmond.com/news/local/", "tag": "h3", "class": "tnt-headline"}
    }
    headers = {'User-Agent': 'Mozilla/5.0'}
    total_stress = 0
    
    st.header("🏠 Local Campus & City News")
    
    for name, info in sources.items():
        try:
            response = requests.get(info["url"], headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = soup.find_all(info["tag"], class_=info["class"])
            if not headlines: headlines = soup.select(f"{info['tag']} a")

            st.write(f"### 📍 {name.upper()}")
            for h in headlines[:10]:
                text = h.get_text().strip()
                total_stress += scan_for_stress(text)
                link_tag = h.find('a') if h.name != 'a' else h
                full_link = urljoin(info["url"], link_tag['href']) if link_tag else None
                
                with st.expander(f"📌 {text}"):
                    if full_link:
                        lead = get_article_lead(full_link)
                        st.write(f"*{lead}*")
                        st.markdown(f"[Read Full Story]({full_link})")
                    else:
                        st.write("No link available.")
        except:
            st.error(f"⚠️ Could not connect to {name}.")
    return total_stress

def fetch_global_news():
    total_stress = 0
    st.header("🌍 Global Headlines")
    
def fetch_global_news():
    total_stress = 0
    st.header("🌍 Global Headlines")
    
    # 1. THE ECONOMIST (UNDER CONSTRUCTION)
    st.write("### 📈 THE ECONOMIST")
    st.info("🚧 **Section Under Construction:** We are currently refining the scraper to handle The Economist's premium paywall and security layers.")
    
    # --- COMMENTED OUT ECONOMIST LOGIC ---
    # try:
    #     url = "https://www.economist.com/latest" 
    #     headers = {'User-Agent': 'Mozilla/5.0'}
    #     response = requests.get(url, headers=headers, timeout=10)
    #     # Logic for parsing economist content goes here in future updates
    # except Exception as e:
    #     pass
    # -------------------------------------

    st.divider()

    # 2. NEW YORK TIMES (API - Active & Reliable)
    st.write("### 📰 NEW YORK TIMES")
    nyt_url = f"https://newsdata.io/api/1/latest?apikey={API_KEY}&language=en&domainurl=nytimes.com"
    try:
        response = requests.get(nyt_url)
        data = response.json()
        if data.get("status") == "success":
            for article in data.get("results", [])[:8]:
                title = article.get('title', '')
                description = article.get('description', 'No leade available.')
                total_stress += scan_for_stress(title)
                with st.expander(f"🌐 {title}"):
                    st.write(f"*{description}*")
                    st.markdown(f"[Read Story]({article.get('link')})")
        else:
            st.error("❌ NYT API limit reached.")
    except:
        st.error("⚠️ NYT Connection failed.")
        
    return total_stress

    # 2. NEW YORK TIMES (API - Reliable Backup)
    st.write("### 📰 NEW YORK TIMES")
    nyt_url = f"https://newsdata.io/api/1/latest?apikey={API_KEY}&language=en&domainurl=nytimes.com"
    try:
        response = requests.get(nyt_url)
        data = response.json()
        if data.get("status") == "success":
            for article in data.get("results", [])[:8]:
                title = article.get('title', '')
                description = article.get('description', 'No leade available.')
                total_stress += scan_for_stress(title)
                with st.expander(f"🌐 {title}"):
                    st.write(f"*{description}*")
                    st.markdown(f"[Read Story]({article.get('link')})")
        else:
            st.error("❌ NYT API limit reached.")
    except:
        st.error("⚠️ NYT Connection failed.")
        
    return total_stress

# --- 3. THE DISPLAY ---

def display_cognitive_load(load_score):
    st.subheader("🧠 Cognitive Load")
    st.progress(load_score / 100)
    if load_score > 70:
        st.warning(f"Load: {load_score}% - High Stress Detected. System 1 (Reactive) is dominant.")
    else:
        st.success(f"Load: {load_score}% - Equanimity maintained. System 2 (Mindful) in control.")

def run_scout():
    st.title("☀️ NEWS SCOUT DASHBOARD")
    st.write("For George | URMindful")
    
    if st.button("Run News Scout"):
        cumulative_stress = 0
        cumulative_stress += pull_local_news()
        cumulative_stress += fetch_global_news()
        
        st.divider()
        display_cognitive_load(min(100, cumulative_stress))
        st.balloons()

if __name__ == "__main__":
    run_scout()