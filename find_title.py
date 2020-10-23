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
    try:
        year = int(soup.find('span', attrs={'id':'titleYear'}).a.text)
    except AttributeError:
        year = None
    try:
        cert = next(soup.find('div', class_='subtext').children).strip()
    except AttributeError:
        cert = None
    # time = int(soup.find('h4', text='Runtime:').next_sibling.next_sibling.text[:-3])
    try:
        rating = float(soup.find('span', attrs={'itemprop':'ratingValue'}).text)
    except AttributeError:
        rating = None
    try:
        meta = int(soup.find('div', class_='metacriticScore score_mixed titleReviewBarSubItem').text)
    except AttributeError:
        meta = None
    try:
        hs = soup.find_all('h4', attrs={'class':'inline'})
        for h in hs:
            if 'Gross USA' in h.text:
                gross = int(h.next_sibling.replace(',', '').strip()[1:])
                break
        else:
            gross = None
    except AttributeError:
        gross = None
    try:
        votes = int(soup.find('span', attrs={'itemprop':'ratingCount'}).text.replace(',', ''))
    except AttributeError:
        votes = None
    try:
        genres = list(set(x.text.strip() for x in soup.find_all('a', href=re.compile('genres'))))
    except AttributeError:
        genres = None
    try:
        description = soup.find('div', attrs={'class':'inline canwrap'}).text.strip()
    except AttributeError:
        description = None
    
    print(year, cert, rating, meta, gross, votes, genres, description)
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


