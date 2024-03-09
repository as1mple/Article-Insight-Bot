from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent

from modules.models.article import Article, DailyArticles


class HabrArticleParserHandler:
    BASE_URL = "https://habr.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json, text/plain, */*',
            'user-Agent': UserAgent().google,
        })

    def get_top_articles(self) -> DailyArticles:
        response = self.session.get(f"{self.BASE_URL}/ru/top/daily")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        all_hrefs_articles = soup.find_all('a', class_='tm-title__link')
        articles_list = [
            Article(title=article.find('span').text, link=f"https://habr.com{article.get('href')}")
            for article in all_hrefs_articles
        ]
        return DailyArticles(articles=articles_list)

    def get_content(self, link: str) -> str:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.find_all(class_='article-formatted-body article-formatted-body article-formatted-body_version-2')[0]
        return content.text

    def save_to_json(self, path_to_save, data: dict) -> None:
        with open(path_to_save, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
