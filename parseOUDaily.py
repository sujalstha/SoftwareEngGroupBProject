import requests  # request website
from bs4 import BeautifulSoup  # html scrape
import re  # for text "\n" * (n amt of times) reoccurrence formatting
from urls import urls as URLS

class ArticleScraper:
    def __init__(self):
        # Mozilla or Chrome doesn't matter, Mozilla is more reliable
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def scrape(self, url):
        # fetch webpage
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # get title
        title = soup.select_one("h1")
        title_text = title.get_text(strip=True) if title else "No title found"

        # get article content
        article = soup.find("div", {"id": "article-body"})
        content_text = article.get_text("\n", strip=True) if article else "No content found"

        # remove subscription text
        newsletter_markers = [
            "NEWSLETTERS",
            "A few times a week",
            "FREE SIGN UP",
            "Subscribing",
            "NEWSLETTERS\n* required",
            "Subscribing...",
            "Thank you for subscribing!"
        ]
        for marker in newsletter_markers:
            if marker in content_text:
                content_text = content_text.split(marker)[0].strip()

        # remove editor footnote text
        footer_markers = [
            "This story was edited by",
            "Commenting policy:",
            "MAKE US A GOOGLE PREFERRED SOURCE",
            "COMPLETE ONE-STEP PROCESS"
        ]
        for marker in footer_markers:
            if marker in content_text:
                content_text = content_text.split(marker)[0].strip()
                break

        # removes multiple blank lines
        content_text = re.sub(r"\n{2,}", "\n\n", content_text)

        return title_text, content_text


if __name__ == "__main__":
    scraper = ArticleScraper()

    for url in URLS:
        title_text, content_text = scraper.scrape(url)

        print("\n--- URL ---")
        print(url)
        print("\n---Article Title---\n", title_text)
        print("\n---Article Content---\n", content_text)
        print("\n")
