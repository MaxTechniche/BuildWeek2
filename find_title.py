import re
import requests

import bs4
from bs4 import BeautifulSoup

from pprint import pprint
from collections import OrderedDict



def get_title_info(title):
    imdb_title_page = 'https://www.imdb.com' + title
    source = requests.get(imdb_title_page).text
    soup = BeautifulSoup(source, 'lxml')

    all_info = {}

    # title_ = next(soup.find('h1', attrs={'class':''}).children)[:-1]
    year = int(soup.find('span', attrs={'id':'titleYear'}).a.text)
    try:
        cert = next(soup.find('div', class_='subtext').children).strip()
    except AttributeError:
        cert = None
    # time = int(soup.find('h4', text='Runtime:').next_sibling.next_sibling.text[:-3])
    rating = float(soup.find('span', attrs={'itemprop':'ratingValue'}).text)
    try:
        meta = int(soup.find('div', class_='metacriticScore score_mixed titleReviewBarSubItem').text)
    except AttributeError:
        meta = None
    try:
        hs = soup.find_all('h4', attrs={'class':'inline'})
        for h in hs:
            if 'USA' in h.text:
                gross = int(h.next_sibling.replace(',', '').strip()[1:])
                break
        else:
            gross = None
    except AttributeError:
        gross = None
    votes = int(soup.find('span', attrs={'itemprop':'ratingCount'}).text.replace(',', ''))
    genres = list(set(x.text.strip() for x in soup.find_all('a', href=re.compile('genres'))))
    description = soup.find('div', attrs={'class':'inline canwrap'}).text.strip()
    
    return year, cert, rating, meta, gross, votes, genres, description



def get_titles(query, one=False):
    if not query:
        return None
    imdb_search = 'https://www.imdb.com/find?q='
    movies = '&s=tt&ttype=ft'
    source = requests.get(imdb_search + str(query) + movies).text
    soup = BeautifulSoup(source, 'lxml')
    
    data = soup.find('div', class_='findSection')
    if data:
        if 'Titles' not in data.h3.text:
            return None
    else:
        return None

    x = 5
    if one:
        x = 1

    titles = OrderedDict()
    for title in data.find_all('td', 'result_text')[:x]:
        titles[title.text] = title.a['href']
    return titles


