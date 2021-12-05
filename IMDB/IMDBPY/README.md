Query is based on IMDbPY lib.

Source file is included for lib but need to create our own lib to implement changes

Multiple commenting is created for different output

# Terminal installation

pip install IMDbPY

# Queries for IMDbPY

search_movie(title):
    Returns movie title, year and id

search_episode(title):
    Searches for titles of TV series episodes.

get_movie(movieID):
    Returns Movie Object
    use movieObject['cast'] for list of actor and actresses

# Identical Queries for IMDbPy

search_person(name), get_person(personID), search_character(name), get_character(characterID),search_company(name), get_company(companyID)

# Queries for keyword search

search_keyword(string), get_keyword(keyword)

# Queries for returning url

get_imdbURL(Movie/person/character/companyobject)
    returns IMDB url for the given object
