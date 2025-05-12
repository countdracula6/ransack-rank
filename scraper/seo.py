import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service

STOPWORDS = set("""
the is in and to of a an for with on at by it from this that be or as are was were but if not you your their its which has have can will do does had
""".split())

def take_screenshot(url, filename):
    try:
        options = FirefoxOptions()
        options.headless = True
        service = Service(executable_path="/snap/bin/geckodriver")
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_window_size(1366, 768)
        driver.get(url)
        screenshot_path = os.path.join("static/screenshots", filename)
        driver.save_screenshot(screenshot_path)
        driver.quit()
        return screenshot_path
    except Exception as e:
        print("Screenshot error:", e)
        return None

def analyze_seo(url, target_keyword=None):
    result = {
        "title": None,
        "description": None,
        "h1_count": 0,
        "h2_count": 0,
        "h3_count": 0,
        "word_count": 0,
        "image_count": 0,
        "missing_alt": 0,
        "canonical": None,
        "robots": None,
        "og_title": None,
        "twitter_card": None,
        "top_keywords": {},
        "screenshot": None,
        "keyword_density": None
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # Screenshot
        domain = re.sub(r'\W+', '', url.replace("https://", "").replace("http://", ""))[:40]
        filename = f"{domain}.png"
        result["screenshot"] = take_screenshot(url, filename)

        # Title
        result["title"] = soup.title.string.strip() if soup.title else "N/A"

        # Meta description
        desc = soup.find("meta", attrs={"name": "description"})
        result["description"] = desc['content'].strip() if desc and desc.get("content") else "N/A"

        # Headings
        result["h1_count"] = len(soup.find_all("h1"))
        result["h2_count"] = len(soup.find_all("h2"))
        result["h3_count"] = len(soup.find_all("h3"))

        # Text content
        text = soup.get_text(separator=" ")
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        filtered_words = [word for word in words if word not in STOPWORDS]
        word_freq = Counter(filtered_words).most_common(10)

        result["word_count"] = len(words)
        result["top_keywords"] = dict(word_freq)

        # Images
        images = soup.find_all("img")
        result["image_count"] = len(images)
        result["missing_alt"] = sum(1 for img in images if not img.get("alt"))

        # Canonical
        link_tag = soup.find("link", rel="canonical")
        result["canonical"] = link_tag["href"] if link_tag and link_tag.get("href") else "N/A"

        # Robots
        robots_tag = soup.find("meta", attrs={"name": "robots"})
        result["robots"] = robots_tag["content"] if robots_tag and robots_tag.get("content") else "N/A"

        # Open Graph
        og_tag = soup.find("meta", property="og:title")
        result["og_title"] = og_tag["content"] if og_tag and og_tag.get("content") else "N/A"

        # Twitter card
        tw_card = soup.find("meta", attrs={"name": "twitter:card"})
        result["twitter_card"] = tw_card["content"] if tw_card and tw_card.get("content") else "N/A"

        # Keyword Density Logic
        if target_keyword:
            keyword = target_keyword.lower().strip()
            count = sum(1 for word in words if word == keyword)
            percent = (count / len(words)) * 100 if words else 0

            tag_hits = {
                "title": keyword in result["title"].lower() if result["title"] else False,
                "description": keyword in result["description"].lower() if result["description"] else False,
                "h1": any(keyword in h.get_text(strip=True).lower() for h in soup.find_all("h1")),
                "h2": any(keyword in h.get_text(strip=True).lower() for h in soup.find_all("h2")),
                "h3": any(keyword in h.get_text(strip=True).lower() for h in soup.find_all("h3"))
            }

            result["keyword_density"] = {
                "keyword": keyword,
                "count": count,
                "percent": round(percent, 2),
                "tags": tag_hits
            }

    except Exception as e:
        result["error"] = str(e)

    return result
