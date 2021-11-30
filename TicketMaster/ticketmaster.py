import ticketpy 

tm_client_key = ticketpy.ApiClient('cIOC1j1MrGAdAUJ768mJuXRQSikHPKGY')

"""
#Search Query
country = input("Enter country code: ")
state = input("Enter State Code: ")
city = input ("Enter City Name: ")
"""

#Event Output
#For limit we need to remove the loop and connect event directly.

Events = tm_client_key.events.find(
    #classification_name='Rock , Hip-Hop',
    country_code= 'US',
    #state_code= 'TX',
    #city = 'Dallas',
    start_date_time='2021-11-17T10:00:00Z',
    end_date_time='2021-12-18T23:00:00Z'
) #.limit(10)

for pages in Events:
    for event in pages:
        print(event)
        
"""
#Venue Output
Venues = tm_client_key.venues.find(
    country_code='US',
)

#Venues = tm_client_key.venues.find(keyword="Wolf").all()

for pages in Venues:
    for venue in pages:
        print(venue)
#for venue in Venues:
    #print("Name: {} / City: {}".format(venue.name, venue.city))

"""

