import requests
from bs4 import BeautifulSoup

def analyze_seo(url):
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
        "twitter_card": None
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # Title
        result["title"] = soup.title.string.strip() if soup.title else "N/A"

        # Meta description
        desc = soup.find("meta", attrs={"name": "description"})
        result["description"] = desc['content'].strip() if desc and desc.get("content") else "N/A"

        # Headings
        result["h1_count"] = len(soup.find_all("h1"))
        result["h2_count"] = len(soup.find_all("h2"))
        result["h3_count"] = len(soup.find_all("h3"))

        # Word count
        text = soup.get_text(separator=" ")
        result["word_count"] = len(text.split())

        # Images
        images = soup.find_all("img")
        result["image_count"] = len(images)
        result["missing_alt"] = sum(1 for img in images if not img.get("alt"))

        # Canonical
        link_tag = soup.find("link", rel="canonical")
        result["canonical"] = link_tag["href"] if link_tag and link_tag.get("href") else "N/A"

        # Robots meta
        robots_tag = soup.find("meta", attrs={"name": "robots"})
        result["robots"] = robots_tag["content"] if robots_tag and robots_tag.get("content") else "N/A"

        # Open Graph title
        og_tag = soup.find("meta", property="og:title")
        result["og_title"] = og_tag["content"] if og_tag and og_tag.get("content") else "N/A"

        # Twitter card type
        tw_card = soup.find("meta", attrs={"name": "twitter:card"})
        result["twitter_card"] = tw_card["content"] if tw_card and tw_card.get("content") else "N/A"

    except Exception as e:
        result["error"] = str(e)

    return result
