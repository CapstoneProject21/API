from Authclient import *
from Query import *
from TicketModel import *

tm_client_key = API_Client('cIOC1j1MrGAdAUJ768mJuXRQSikHPKGY')

Events = tm_client_key.events.find(
    classification_name='Rock , Hip-Hop',
    state_code= 'TX',
    city = 'Dallas',
    start_date_time='2021-11-17T10:00:00Z',
    end_date_time='2021-12-18T23:00:00Z'
)

for pages in Events:
    for event in pages:
        print(event)