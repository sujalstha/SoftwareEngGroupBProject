# Sujal Shrestha

import requests # request website
from bs4 import BeautifulSoup # html scrape
import re # for text "\n" * (n amt of times) reoccurrence formatting

class ArticleScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"} # Mozilla or Chrome doesn't matter, Mozilla is more reliable

    def scrape(self, url):
        # fetch webpage
        response = requests.get(url, headers=self.headers)
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
    urls = [
        "https://www.oudaily.com/news/ou-statement-student-failing-grade-bible-psychology-essay-discrimination-first-amendment/article_306d35a7-ac6a-433f-9ff9-8dad255b1b72.html",
        "https://www.oudaily.com/news/ou-football-playoff-final-exams-graduation-conflict-fall-2025/article_f57b5989-2c7a-4727-a13c-0346228da07a.html",
        "https://www.oudaily.com/news/ou-wasps-catlett-music-center/article_d70e9ca4-357e-46b0-bccb-66e114db2d19.html",
        "https://www.oudaily.com/news/ou-norman-health-campus-graduate-college-university-libraries/article_da20e831-5a8d-4dd1-9d70-0d50c3b9b881.html",
        "https://www.oudaily.com/news/ou-undergraduate-student-congress-sga/article_cd8b6897-af2f-436b-ba0c-f514b0241ad0.html",
        "https://www.oudaily.com/news/ou-communications-professor-resignation-alleged-harassment/article_5b619b9a-f849-412e-9584-bbc0e36d018e.html",
        "https://www.oudaily.com/news/cleveland-county-norman-power-outage/article_565a4623-0924-4fea-84e7-b8f68afd5e1a.html",
        "https://www.oudaily.com/news/ou-sga-undergraduate-student-congress/article_a3906e63-fdd4-4236-ae7d-45dd0517985d.html",
        "https://www.oudaily.com/news/pride-of-oklahoma-boone-pickens-el-sistema-oklahoma/article_eab839ca-09f8-41d2-81b7-dfbfc5d00498.html",
        "https://www.oudaily.com/news/ou-housing-traditions-east-mccasland-freshman-off-campus/article_b1995171-fd2c-429d-afff-6354637f44a7.html",
        "https://www.oudaily.com/news/ou-parking-transportation-director-growth/article_15ca790b-50de-4794-adb7-64e68143cd26.html",
        "https://www.oudaily.com/news/conservative-commentator-steven-crowder-prove-me-wrong-law-enforcement-steven-crowder/article_bbc2f062-33e4-4a41-b946-019b268f7bdf.html",
        "https://www.oudaily.com/news/ou-skate-club-first-skate-competition-texas-am/article_ac78cd4e-089f-469c-9830-1071358e2e0f.html",
        "https://www.oudaily.com/news/ou-chief-ai-officer-shishir-shah/article_48e1ed61-92fa-4db9-a1bd-0740577f668c.html",
        "https://www.oudaily.com/news/ou-university-library-bizzell-modernization-improvements/article_cf163c37-4ddb-4259-91bd-31c8c0fd17c5.html",
        "https://www.oudaily.com/sports/oklahoma-sooners-football-sec-travon-hall-krew-jones/article_a2beb15e-ae0a-4509-abeb-7903ba3fa07d.html",
        "https://www.oudaily.com/sports/oklahoma-sooners-football-sec-ap-poll-college-football-playoffs/article_365e3440-1d44-4d76-9a1e-7c515bf57259.html",
        "https://www.oudaily.com/sports/ou-football-recruiting-tracker/collection_a1bcec7d-9d99-44ed-8716-fc4b98833fa6.html",
        "https://www.oudaily.com/sports/oklahoma-sooners-football-sec-john-mateer-lsu-college-football-playoffs/article_dfc7eaf5-1e71-4453-9ac7-1533ac30968b.html",
        "https://www.oudaily.com/sports/ou-oklahoma-sooners-football-sec-lsu-isaiah/article_d45f9728-d383-4f8f-8091-7425ada64d90.html",
        "https://www.oudaily.com/sports/ou-oklahoma-sooners-football-sec-lsu-key-plays-college-football-playoffs-isaiah-sategna-peyton-bowen/article_d37292ec-77d6-4be5-a0f2-a111cd1eec62.html",
        "https://www.oudaily.com/sports/oklahoma-sooners-football-sec-lsu-college-football-playoffs/article_9e8d1df9-2e01-4f40-b839-9b297c5493f6.html",
        "https://www.oudaily.com/sports/r-mason-thomas-jayden-jackson-lsu-sec-availability-ou-football-oklahoma-sooners-injury-report/article_c7fafc16-8e1b-43b6-8a66-461a707bde05.html",
        "https://www.oudaily.com/sports/ou-oklahoma-sooners-football-former-quarterback-jalen-hurts-philadelphia-eagles-chicago-bears/article_e4a112a8-6761-4dac-afe0-3c967ae2611a.html",
        "https://www.oudaily.com/sports/ou-oklahoma-sooners-football-sec-commit-class-of-2026-dane-bathurst/article_7d09a5f5-3c33-4b22-845d-e4670b3a343e.html",
        "https://www.oudaily.com/sports/oklahoma-sooners-football-sec-markel-ford-jonathan-hatton-jr/article_e2d12ff0-447e-43b0-9f69-092493d737cd.html",
        "https://www.oudaily.com/sports/ou-oklahoma-sooners-football-sec-missouri-lsu-kendal-daniels-kip-lewis/article_4b97bfd1-ce70-4fd6-9696-f69b15e76303.html",
        "https://www.oudaily.com/sports/oklahoma-sooners-football-sec-college-football-playoffs-missouri-lsu/article_8cd1910b-d9ac-4893-8920-e9960f86ba61.html",
        "https://www.oudaily.com/sports/ou-oklahoma-sooners-football-sec-peyton-eli-bowen-jim-thorpe-award-national-defensive-back-of-the-week/article_f0604eb6-de8b-4bed-bb86-adea9c2dc69c.html",
        "https://www.oudaily.com/sports/oklahoma-football-sooners-john-mateer-lsu-college-football-playoffs/article_8bf15dc8-959b-40c5-9f89-85469aefd0e1.html",
        "https://www.oudaily.com/sports/ou-oklahoma-sooners-football-nfl-baker-mayfield-tampa-bay-buccanneers-los-angeles-rams/article_99ccb786-6ced-4357-acb4-9dc1d4da8a75.html",
        "https://www.oudaily.com/sports/ou-oklahoma-sooners-womens-basketball-ap-poll-sec/article_3f1a833a-d6cc-4b1f-b599-5dbc5c46140e.html",
        "https://www.oudaily.com/sports/oklahoma-football-sooners-sec-keontez-lewis-texas-missouri/article_be04aeec-b419-4bf7-af4e-2f2852c31389.html",
        "https://www.oudaily.com/sports/dr-steven-shin-john-mateer-oklahoma-football-sooners-sec-missouri/article_216fa0a4-9d19-4d0e-be54-0ba730b3c59f.html",
    ]
    scraper = ArticleScraper()

    for url in urls:
        title_text, content_text = scraper.scrape(url)

        print("\n--- URL ---")
        print(url)
        print("\n---Article Title---\n", title_text)
        print("\n---Article Content---\n", content_text)
        print("\n")
