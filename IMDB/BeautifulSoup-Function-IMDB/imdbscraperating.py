#BeautifulSoup = scraping api data xml and html

import requests
import re
from bs4 import BeautifulSoup
import json

#Top 250 movie's data
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
scrape = BeautifulSoup(response.text, 'lxml')

#using BeautifulSoup to extract movie details from Beautiful Soup Object using Html tags like href, title, data-value
movies = scrape.select('td.titleColumn')
links = [a.attrs.get('href') for a in scrape.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in scrape.select('td.titleColumn a')]
 
ratings = [b.attrs.get('data-value')
           for b in scrape.select('td.posterColumn span[name=ir]')]
 
votes = [b.attrs.get('data-value')
         for b in scrape.select('td.ratingColumn strong')]

#creating empty list 

list = []

#Iterating and extracting

for index in range(0, len(movies)):
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index))-(len(movie))]
    data = {"movie_title": movie_title,
            "year": year,
            "place": place,
            "star_cast": crew[index],
            "rating": ratings[index],
            "vote": votes[index],
            "link": links[index]}
    list.append(data)

#print command
for movie in list:
    dict = {
        "Rank" : movie['place'],
        "Title" : movie['movie_title'],
        "Year" : movie['year'],
        "Starting" : movie['star_cast'],
        "Rating" : movie['rating'],
        #"Vote" : movie['vote']
    }
    #dict = {' Rank:', movie['place'], '\n','Title: ', movie['movie_title'], '\n', 'Year: ', movie['year'], '\n', 'Starring:', movie['star_cast'],'\n','Rating:', movie['rating']}
    imdb_json = json.dumps(dict)
    print(imdb_json)
