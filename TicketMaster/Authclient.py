import logging
import requests
from collections import namedtuple
from urllib import parse
from Ticketmasterpy.Query import (
    EventQuery,
    VenueQuery
)
from Ticketmasterpy import Response

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sf = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(sf)
log.addHandler(sh)

class API_Client:
    root_url = 'https://app.ticketmaster.com'
    url = 'https://app.ticketmaster.com/discovery/v2'

    def __init__(self, api_key):
        self.__api_key = None
        self.api_key = api_key
        self.events = EventQuery(api_client=self)
        self.venues = VenueQuery(api_client=self)
        self.segment_by_id = self.classifications.segment_by_id
        self.genre_by_id = self.classifications.genre_by_id
        self.subgenre_by_id = self.classifications.subgenre_by_id

        log.debug("Root URL: {}".format(self.url))
    
    def search(self, method, **kwargs):
        kwargs = {k: v for (k, v) in kwargs.items() if v is not None}
        updates = self.api_key

        for k, v in kwargs.items():
            if k in ['includeTBA', 'includeTBD', 'includeTest']:
                updates[k] = self.__yes_no_only(v)
            elif k in ['size', 'radius', 'marketId']:
                updates[k] = str(v)
        kwargs.update(updates)
        log.debug(kwargs)
        urls = {
            'events': self.__method_url('events'),
            'venues': self.__method_url('venues'),
        }
        resp = requests.get(urls[method], params=kwargs)
        return Page_Response(self, self._handle_response(resp))

    def handle_response(self, response):
        if response.status_code == 200:
            return self.__success(response)
        elif response.status_code == 401:
            self.__fault(response)
        elif response.status_code == 400:
            self.__error(response)
        else:
            self.__unknown_error(response)
    
    @staticmethod
    def success(response):
        return response.json()
    
    @staticmethod
    def error(response):
        res = response.json()
        error = namedtuple('error', ['code','detail','href'])
        errors = [
            error(er['code'], er['detail'], er['_links']['about']['href'])
            for er in res['errors']
        ]
        log.error('URL: {}\nErrors: {}'.format(response.url, errors))
        raise API_Exception(response.status_code, errors, response.url)
    
    @staticmethod
    def fault(response):
        res = response.json()
        fault_str = res['fault']['faultstring']
        detail = res['fault']['detail']
        log.error('URL: {}, Faultstr: {}'.format(response.url, fault_str))
        raise API_Exception(
            response.status_code,
            fault_str,
            detail,
            response.url
        )
    
    def unknown_error(self, response):
        res = response.json()
        if 'fault' in res:
            self.__fault(response)
        elif 'errors' in res:
            self.__error(response)
        else:
            raise API_Exception(response.status_code, response.text)

    def get_url(self, link):
        link = self._parse_link(link)
        resp = requests.get(link.url, link.params)
        return Response.from_json(self._handle_response(resp))
    
    def _parse_link(self, link):
        parsed_link = namedtuple('link', ['url', 'params'])
        link_url, link_params = link.split('?')
        params = self._link_params(link_params)
        return parsed_link(link_url, params)

    def _link_params(self, param_str):
        search_params = {}
        params = parse.parse_qs(param_str)
        for k, v in params.items():
            search_params[k] = v[0]
        search_params.update(self.api_key)
        return search_params

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key):
        # Set this way by default to pass in request params
        self.__api_key = {'apikey': api_key}

    @staticmethod
    def __method_url(method):
        return "{}/{}.json".format(API_Client.url, method)

    @staticmethod
    def __yes_no_only(s):
        s = str(s).lower()
        if s in ['true', 'yes']:
            s = 'yes'
        elif s in ['false', 'no']:
            s = 'no'
        return s


class API_Exception(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Page_Response:
    def __init__(self, api_client, resp):
        self.api_client = api_client
        self.response = None
        self.response = Response.from_json(resp)

    def limit(self, max_pages=5):
        all_items = []
        counter = 0
        for rp in self:
            if counter >= max_pages:
                break
            counter += 1
            all_items += rp
        return all_items

    def one(self):
        return [i for i in self.response]

    def all(self):
        # TODO Rename this since all() is a built-in function...
        return [i for item_list in self for i in item_list]

    def __iter__(self):
        yield self.response
        next_url = self.response.links.get('next')
        while next_url:
            log.debug("Requesting page: {}".format(next_url))
            rp = self.api_client.get_url(next_url)
            next_url = rp.links.get('next')
            yield rp
        return
