from collections import UserList
from datetime import datetime
import re
from types import DynamicClassAttribute
import Ticketmasterpy

def assign_links(obj, json_obj, base_url=None):
    json_links = json_obj.get('_links')
    if not json_links:
        obj.links = {}
    else:
        obj_links = {}
        for k, v in json_links.items():
            if 'href' in v:
                href = re.sub("({.+)", "", v['href'])
                if base_url:
                    href = "{}{}".format(base_url, href)
                obj_links[k] =href
            else:
                obj_links[k] = v
        obj.links  = obj_links

#API response class

class Response(list):
    def __init__(self, number=None, size=None, total_elements=None, total_pages=None):
        super().__init__([])
        self.number = number
        self.size = size
        self.total_elements = total_elements
        self.total_pages =  total_pages

    @staticmethod
    def from_json(json_obj):
        rp = Response()
        rp.json = json_obj
        assign_links(rp,json_obj, Ticketmasterpy.API_Client.root_url)
        rp.number = json_obj['response']['number']
        rp.size = json_obj['response']['size']
        rp.total_pages = json_obj['response']['pages']
        rp.total_elements = json_obj['response']['elements']

        embedded =  json_obj.get('_embedded')
        if not embedded:
            return rp

        obj_models = {
            'events': Event,
            'venues' : Venue,
        }
        for k, v in embedded.items():
            if k in obj_models:
                obj_type = obj_models[k]
                rp += [obj_type.from_json(obj) for obj in v]
        return rp

    def __str__(self):
        return(
            "Response {number}/{total_pages},"
            "Size: {size},"
            "Total elements: {total_elements}"
        ).format(**self.__dict__)

class Event:
    def __init__(self, event_id=None, name=None,
                start_date=None,start_time=None, status=None, price_ranges=None,
                venues=None, utc_datetime=None, links=None):
        self.id = event_id
        self.name = name
        #(YYYY-MM-DD)
        self.local_start_date = start_date
        #(HH:MM:SS)
        self.local_start_time =  start_time
        self.status = status
        self.price_ranges = price_ranges
        self.venues = venues
        self.links = links
        self.__utc_datetime = None
        if utc_datetime is not None:
            self.utc_datetime =  utc_datetime
    
    @property
    def utc_datetime(self):
        """Start date/time in UTC (*YYYY-MM-DDTHH:MM:SSZ*)"""
        return self.__utc_datetime

    @utc_datetime.setter
    def utc_datetime(self, utc_datetime):
        if not utc_datetime:
            self.__utc_datetime = None
        else:
            ts_format = "%Y-%m-%dT%H:%M:%SZ"
            self.__utc_datetime = datetime.strptime(utc_datetime, ts_format)
    
    @staticmethod
    def from_json(json_event):
        E =  Event()
        E.json = json_event
        E.id = json_event.get('id')
        E.name = json_event.get('name')

        dates = json_event.get('dates', {})
        start_dates =  dates.get('start', {})
        E.local_start_date =  start_dates.get('localDate')
        E.local_start_time = start_dates.get('localTime')
        E.utc_datetime = start_dates.get('dateTime')
        status = dates.get('status', {})
        E.status = status.get('code')

        price_ranges = []
        if 'priceRanges' in json_event:
            for PR in json_event['priceRanges']:
                price_ranges.append({'min': PR['min'], 'max': PR['max']})
            E.price_ranges = price_ranges
        
        venues = []
        if 'venues' in json_event.get('_embedded', {}):
            for v in json_event['_embedded']['venues']:
                venues.append(Venue.from_json(v))
        E.venues = venues
        assign_links(E, json_event)
        return E

    def __str__(self):
        tmpl = ("Event:            {name}\n"
                "Venues:           {venues}\n"
                "Start date:       {local_start_date}\n"
                "Start time:       {local_start_time}\n"
                "Price ranges:     {price_ranges}\n"
                "Status:           {status}\n")
                
        return tmpl.format(**self.__dict__)


class Venue:
    def __init__(self, name=None, address=None, city=None, state_code=None,
                postal_code=None, latitude=None, longitude =None, markets=None,
                url= None, box_office_info=None, dmas = None,general_info=None, venue_id=None,social=None, timezone=None, images=None,
                parking_detail=None, accessible_seating_detail=None, links = None):

        self.name = name
        self.id = venue_id
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.state_code = state_code
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.url = url 
        self.box_office_info = box_office_info
        self.dmas = dmas
        self.markets = markets
        self.general_info = general_info
        self.social = social
        self.images = images
        self.parking_detail = parking_detail
        self.accessible_seating_detail = accessible_seating_detail
        self.links = links

    @property
    def location(self):
        """Location-based data (full address, lat/lon, timezone"""
        return {
            'address': self.address,
            'postal_code': self.postal_code,
            'city': self.city,
            'state_code': self.state_code,
            'timezone': self.timezone,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    @staticmethod
    def from_json(json_venue):
        """Returns a ``Venue`` object from JSON"""
        V = Venue()
        V.json = json_venue
        V.id = json_venue.get('id')
        V.name = json_venue.get('name')
        V.url = json_venue.get('url')
        V.postal_code = json_venue.get('postalCode')
        V.general_info = json_venue.get('generalInfo')
        V.box_office_info = json_venue.get('boxOfficeInfo')
        V.dmas = json_venue.get('dmas')
        V.social = json_venue.get('social')
        V.timezone = json_venue.get('timezone')
        V.images = json_venue.get('images')
        V.parking_detail = json_venue.get('parkingDetail')
        V.accessible_seating_detail = json_venue.get('accessibleSeatingDetail')

        if 'markets' in json_venue:
            V.markets = [m.get('id') for m in json_venue.get('markets')]
        if 'city' in json_venue:
            V.city = json_venue['city'].get('name')
        if 'address' in json_venue:
            V.address = json_venue['address'].get('line1')
        if 'location' in json_venue:
            V.latitude = json_venue['location'].get('latitude')
            V.longitude = json_venue['location'].get('longitude')
        if 'state' in json_venue:
            V.state_code = json_venue['state'].get('stateCode')

        assign_links(V, json_venue)
        return V
    
    def __str__(self):
        return ("{name} at {address} in "
                "{city} {state_code}").format(**self.__dict__)
