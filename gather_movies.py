import re
from shutil import Error
import requests
import pandas as pd
import numpy as np

import bs4
from bs4 import BeautifulSoup

from pprint import pprint

top_base = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&start="

def get_items():
    items = []
    for i in range(1, 1000, 50):
        site = requests.get(top_base + str(i)).text
        movies = BeautifulSoup(site, 'lxml').findAll('div', attrs={'class':'lister-item-content'})
        items.extend(movies)
    return items

items = get_items()


def parse_dict(items):
    movies = []
    for index, item in enumerate(items, 1):
        all_info = {}

        all_info['Placement'] = index
        all_info['Title'] = item.h3.a.text
        all_info['Year'] = int(item.h3.findAll('span')[1].text.rstrip(')')[-4:])
        
        ps = item.findAll('p')
        
        try:
            all_info['Certification'] = ps[0].find('span', class_='certificate').text.strip()
        except AttributeError:
            all_info['Certification'] = np.NaN

        print(index)

        all_info['Runtime'] = int(ps[0].find('span',class_='runtime').text[:-3])
        
        all_info['Genres'] = ps[0].find('span',class_='genre').text.strip().split(', ')
        
        rs = item.find('div')

        all_info['Rating'] = float(rs.strong.text.strip())
        try:
            all_info['Metascore'] = int(rs.findAll('div')[4].span.text.strip())
        except IndexError:
            all_info['Metascore'] = np.NaN
        all_info['Description'] = ps[1].text.strip()

        director_list = []
        stars_list = []
        ds = ps[2]
        directors = False
        stars = False
        for child in list(ds.children):
            if type(child) == bs4.element.NavigableString:
                if child.strip() in ['Directors:', 'Director:']:
                    directors = True
                    stars = False
                elif child.strip() == 'Stars:':
                    stars = True
                    directors = False
                elif not len(child.strip()):
                    directors = False
                    stars = False
                continue

            if directors:
                director_list.append(child.text)
            if stars:
                stars_list.append(child.text)

        all_info['Directors'] = director_list
        all_info['stars'] = stars_list

        nums = ps[3].findAll('span')[1::3]
        
        all_info['Votes'] = int(nums[0]['data-value'])
        try:
            all_info['USA Box Office'] = int(nums[1]['data-value'].replace(',',''))
        except IndexError:
            all_info['USA Box Office'] = np.NaN
        movies.append(all_info)

    return movies

movies = parse_dict(items)

movies = pd.DataFrame.from_dict(movies)
# movies.to_csv('top_1000.csv', index=False)
