import requests
from Ticketmasterpy import Venue, Event

class BaseQuery:
    attribute_map = {
         'start_date_time': 'startDateTime',
        'end_date_time': 'endDateTime',
        'onsale_start_date_time': 'onsaleStartDateTime',
        'onsale_end_date_time': 'onsaleEndDateTime',
        'country_code': 'countryCode',
        'state_code': 'stateCode',
        'venue_id': 'venueId',
        'attraction_id': 'attractionId',
        'segment_id': 'segmentId',
        'segment_name': 'segmentName',
        'classification_name': 'classificationName',
        'classification_id': 'classificationId',
        'market_id': 'marketId',
        'promoter_id': 'promoterId',
        'dma_id': 'dmaId',
        'include_tba': 'includeTBA',
        'include_tbd': 'includeTBD',
        'client_visibility': 'clientVisibility',
        'include_test': 'includeTest',
        'keyword': 'keyword',
        'id': 'id',
        'sort': 'sort',
        'page': 'page',
        'size': 'size',
        'locale': 'locale',
        'latlong': 'latlong',
        'radius': 'radius'       
    }

    def __init__(self, api_client, method, model):
        self.api_client = api_client
        self.method = method
        self.model = model
    
    def __get(self, **kwargs):
        response = self.apiP_client.search(self.method, **kwargs)
        return response

    def _get(self, keyword=None, entity_id=None, sort=None, in_test=None,
             page=None, size=None, locale=None, **kwargs):
        
        search_args= dict(kwargs)
        search_args.update({
            'keyword': keyword,
            'id': entity_id,
            'sort': sort,
            'in_test': in_test,
            'page': page,
            'size': size,
            'locale': locale
        })

        params = self.search_params(**search_args)
        return self.__get(**params)

    def Byid(self, entity_id):
        get_tmpl = "{}/{}/{}"
        get_url = get_tmpl.format(self.api_client.url, self.method, entity_id)
        r = requests.get(get_url, params=self.api_client.api_key)
        r_json = self.api_client._handle_response(r)
        return self.model.from_json(r_json)

    def search_params(self, **kwargs):
        kw_map = {}
        for k, v in kwargs.items():
            if k in self.attribute_map.keys():
                kw_map[self.attribute_map[k]] = v
            elif k in self.attribute_map.values():
                kw_map[k] = v
            else:
                kw_map[k] = v
        
        return {k: v for (k,v) in kw_map.items() if v is not None}

class EventQuery(BaseQuery):

    #omitted classes=>attraction_id=None, segment_id=None, segment_name=None,classification_name=None, classification_id=None,
             
    def __init__(self, api_client):
        super().__init__(api_client, 'events', Event)
    
    def find(self, sort='date,asc', latlong=None, radius=None, unit=None,
             start_date_time=None, end_date_time=None,
             onsale_start_date_time=None, onsale_end_date_time=None,
             country_code=None, state_code=None, venue_id=None,
             market_id=None, promoter_id=None, dma_id=None,
             include_tba=None, include_tbd=None, client_visibility=None,
             keyword=None, event_id=None, source=None, in_test=None,
             page=None, size=None, locale=None, **kwargs):
        
        return self._get(keyword, event_id, sort, in_test, page,
                         size, locale, latlong=latlong, radius=radius,
                         unit=unit, start_date_time=start_date_time,
                         end_date_time=end_date_time,
                         onsale_start_date_time=onsale_start_date_time,
                         onsale_end_date_time=onsale_end_date_time,
                         country_code=country_code, state_code=state_code,
                         venue_id=venue_id, market_id=market_id, 
                         promoter_id=promoter_id, dma_id=dma_id, include_tba=include_tba,
                         include_tbd=include_tbd, source=source,
                         client_visibility=client_visibility, **kwargs)

    def Bylocation(self, latitude, longitude, radius= '30', unit = 'miles', sort = 'relevance,asc', **kwargs):
        latitude = str(latitude)
        longitude = str(longitude)
        radius = str(radius)
        latlong = "{lat},{long}".format(lat=latitude, long=longitude)
        return self.find(
            latlong = latlong,
            radius = radius,
            unit = unit,
            sort = sort,
            **kwargs
        )

class VenueQuery(BaseQuery):
    def __init__(self, api_client):
        super().__init__(api_client, 'venues', Venue)
    
    def find(self, keyword=None, venue_id=None, sort=None, state_code=None,
             country_code=None, source=None, in_test=None,
             page=None, size=None, locale=None, **kwargs):

        return self.get(keyword, venue_id, sort, in_test, page, size,
                        locale, state_code = state_code, country_code = country_code,
                        source = source, **kwargs)
    
    def Byname(self, venue_name, state_code=None, **kwargs):
        return self.find(keyword=venue_name, state_code=state_code, **kwargs)