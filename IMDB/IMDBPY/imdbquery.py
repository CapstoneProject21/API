import imdb

#Creating instance of imdb

ia = imdb.IMDb()

# Query 1
# Search Movie with Year

"""
name = input("Search Movie: ")

search = ia.search_movie(name)


year = search[0]['year']

print(search[0]['title'] + ": " + str(year) )

"""

#Query 2
# Search company name

"""
name = input("Input industry name: ")

search = ia.search_company(name)

for i in range(len(search)):
    id = search[i].companyID

    print(search[i]['name'] + " : " + id)

"""
#Query 3
#Finding info of artists or celebrate

"""
name = input("Enter your celebrate name: ")

celebrate = ia.search_person(name)

celebrate = celebrate[0]

ia.update(celebrate, info = ['biography'])

ia.update(celebrate, info = ['other works'])

print(celebrate['biography'])

print(celebrate['other works'])

"""

#Query 4
#Finding series Episode name
#Implements in Movie but traces back to library which wont be implemented in application.

"""
name = input("Search Series Name: ")

search = ia.search_movie(name)


year = search[0]['year']

id = search[0].movieID

#for i in range(len(search)):
    #id = search[i].movieID

print(search[0]['title'] + ": " + str(year) + " \n ID: " + str(id))

series = ia.get_movie(id)

ia.update(series, 'episodes')

episodes = series.data['episodes']

print("----------")

print(episodes)
"""

# Query 5
# Get name of each episode of series

name = input("Search Series Name: ")

search = ia.search_movie(name)

id = search[0].movieID

series = ia.get_movie(id)

ia.update(series, 'episodes')

episodes = series.data['episodes']

print(series)

for i in episodes.keys():
      
    # Total number of episodes
    n = len(episodes[i])
    
    print("Total Episodes in Season " + str(i) + " : " + str(n))

print("************")

for i in episodes.keys():
      
    # Season Number
    print("Season" + str(i))
      
    # traversing season 
    for j in episodes[i]:
          
        # Title of episode
        title = episodes[i][j]['title']
          
        print(" Ep" + str(j) + " : " + title)

