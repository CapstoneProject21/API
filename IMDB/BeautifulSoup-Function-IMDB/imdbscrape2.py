import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import concurrent.futures
import pandas as pd

# Max number of threads
max_threads = 50

title_arr = []
year_arr = []
genre_arr = []
synopsis_arr =[]
image_url_arr  = []
image_id_arr = []

def getMovieTitle(header):
    try:
        return header[0].find("a").getText()
    except:
        return 'NA'

def getReleaseYear(header):
    try:
        return header[0].find(
            "span",  {
                "class":"lister-item-year text-muted unbold"
                }).getText()
    except:
        return 'NA'

def getGenre(muted_text):
    try:
        return muted_text.find(
            "span",  {
                "class":"genre"
                }).getText()
    except:
        return 'NA'

def getsynopsys(movie):
    try:
        return movie.find_all(
            "p", {
                "class":  "text-muted"
                })[1].getText()
    except:
        return 'NA'

def getImage(image):
    try:
        return image.get(
            'loadlate'
            )
    except:
        return 'NA'

def getImageId(image):
    try:
        return image.get('data-tconst')
    except:
        return 'NA'

def main(imdb_url):
    response = requests.get(imdb_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Movie Name
    movies_list  = soup.find_all(
        "div", {
            "class": "lister-item mode-advanced"
            })
    
    for movie in movies_list:
        header = movie.find_all(
            "h3", {
                "class":  "lister-item-header"
                })
        muted_text = movie.find_all(
            "p", {
                "class":  "text-muted"
                })[0]
        imageDiv =  movie.find(
            "div", {
                "class": "lister-item-image float-left"
                })
        image = imageDiv.find("img", "loadlate")
        
        # Title of Movie
        movie_title =  getMovieTitle(header)
        title_arr.append(movie_title)
        
        # Release year of movie
        year = getReleaseYear(header)
        year_arr.append(year)
        
        # Movie Genre
        genre = getGenre(muted_text)
        genre_arr.append(genre)
        
        # Sypnosys of movies (Movie Detail)
        synopsis = getsynopsys(movie)
        synopsis_arr.append(synopsis)
        
        #  Image attributes
        img_url = getImage(image)
        image_url_arr.append(img_url)
        
        image_id = image.get('data-tconst')
        image_id_arr.append(image_id)

# An array to store all the URL which are queried
imageArr = []

# Maximum number pages to iterate
max_page = 51

# Generates all url

# Movie data only generates movie with English Language and rating from 1.0 to 10.0
# Change langauge and rating will provide more data.

for i in range(0,max_page):
    totalRecords = 0 if i==0 else (250*i)+1
    print(totalRecords)
    imdb_url = f'https://www.imdb.com/search/title/?release_date=2020-01-02,2021-02-01&user_rating=1.0,10.0&languages=en&count=250&start={totalRecords}&ref_=adv_nxt'
    imageArr.append(imdb_url)


#Download Function

def download_data(data_urls):
    threads = min(max_threads, len(data_urls))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(main, data_urls)


# Download function with URLs called imageArr
download_data(imageArr)

# Pandas Dataframe attachment for files.
movieDB = pd.DataFrame({
    "Title": title_arr,
    "Release_Year": year_arr,
    "Genre": genre_arr,
    "Synopsis": synopsis_arr,
    "image_url": image_url_arr,
    "image_id": image_id_arr,
})

print('CSV File Completed')

#Storing File
movieDB.to_csv('IMDB.csv', index=False) 
movieDB.head()
