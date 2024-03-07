from bs4 import BeautifulSoup
import json
import requests
import datetime
from fake_useragent import UserAgent


def get_daily_top_article():
    url = 'https://habr.com/ru/top/daily/'
    ua = UserAgent()

    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-Agent': ua.google,
    }

    article_dict = {}

    req = requests.get(url, headers=headers).text

    soup = BeautifulSoup(req, 'html.parser')
    all_hrefs_articles = soup.find_all('a', class_='tm-title__link')

    for article in all_hrefs_articles:
        article_name = article.find('span').text
        article_link = f'https://habr.com{article.get("href")}'
        article_dict[article_name] = article_link

    with open(f"articles_{datetime.datetime.now().strftime('%d_%m_%Y')}.json", "w", encoding='utf-8') as f:
        try:
            json.dump(article_dict, f, indent=4, ensure_ascii=False)
            print('Done')
        except Exception as e:
            print('Error while writing to file: ', e)
