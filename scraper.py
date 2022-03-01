from bs4 import BeautifulSoup
import os
import requests
import string
import re

base_url = 'https://www.nature.com/nature/articles'

def main():
    number_of_pages = int(input('Enter number of pages to scrape: '))
    type_of_article = input('Enter type of news to scrape: ').lower()

    #make directories
    for num in range(0, number_of_pages):
        if not os.path.isdir('Page_' + str(num + 1)):
            os.mkdir('Page_' + str(num + 1))
        params = {'searchType': 'journalSearch',
                  'sort': 'PubDate', 'year': '2020', 'page': str(num+1)}
        r = requests.get(base_url, params=params)

        if r.status_code != 200:
            print('Error:', r.status_code)
            return

        soup = BeautifulSoup(r.content, 'html.parser')
        spans = soup.find_all('article')

        for span in spans:
            if span.find('span', {'data-test': 'article.type'}
                         ).text.replace('\n', '').lower() == type_of_article:
                news_link = span.find(
                    'a', {'data-track-action': 'view article'}).get('href')
                news_text = get_article_text(
                    'https://www.nature.com' + news_link, type_of_article)
                news_title = span.find(
                    'a', {'data-track-action': 'view article'}).text
                file = open('Page_' + str(num+1) + '/' +
                            format_title(news_title), 'w')
                file.write(news_text)
                file.close()


def format_title(s: str) -> str:
    trans = s.maketrans(' ', '_', string.punctuation)
    s = s.strip()
    s = s.translate(trans)
    s = re.sub('_+', '_', s)
    return s + '.txt'


def get_article_text(url: str, type: str) -> str:
    text_class = 'c-article-body'
    tag = 'div'

    if type == 'news & views' or type == 'research highlights':
        tag = 'main'
        text_class = 'c-article-main-column'

    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r.status_code != 200:
        print('Error:', r.status_code)
        return
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find(tag, {'class': text_class}).text.strip()

if __name__ == '__main__':
    main()
