#!/usr/bin/env python
# coding: utf-8

# In[2]:


import base64
import datetime
from urllib.parse import urlencode

import requests


# In[17]:


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    auth_token= "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_client_credentials(self):
        """returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_cred = f"{client_id}:{client_secret}"
        client_cred_b64 = base64.b64encode(client_cred.encode())
        return client_cred_b64.decode()
        
    def get_token_header(self):
        client_cred_b64 = self.get_client_credentials()
        return{
             "Authorization" : f"Basic {client_cred_b64}"
        }
    def get_token_data(self):
        return{
            "grant_type": "client_credentials"
        }
    
    def Authorization(self):
        auth_token = self.auth_token
        token_data = self.get_token_data()
        token_header = self.get_token_header()
        r = requests.post(auth_token,data=token_data, headers=token_header)
        if r.status_code not in range(200,299):
            raise Exception("could not authenticate client")
            #return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.Authorization()
            return self.get_access_token()
        elif token == None:
            return self.get_access_token()
        return token
    
    def get_resources_header(self):
        access_token = self.get_access_token()
        header = {
            "Authorization": f"Bearer {access_token}"
        }
        return header
    
    def get_resources(self, _id, resource_type="album", version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{_id}"
        header = self.get_resources_header()
        r = requests.get(endpoint, headers=header)
        if r.status_code not in range(200,299):
            return{}
        return r.json()
    
    def get_album(self,_id):
        return self.get_resources(_id,resource_type='albums')
    
    def get_artist(self,_id):
        return self.get_resources(_id,resource_type='artists')
    
    
    def base_search(self, query_parameters, search_type='artists'):
        access_token = self.get_access_token()
        header = {
            "Authorization": f"Bearer {access_token}"
        }
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_parameters}"
        r = requests.get(lookup_url, headers=header)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
        
    def search(self,query= None, operator=None, operator_query=None,search_type='artist'):
        if query == None:
            raise Exception('Query Required')
        if isinstance(query,dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator !=None and operator_query !=None:
            if operator.lower() =="or" or operator.lower() =="not":
                operator = operator.upper()
            if isinstance(operator_query,str):
                query= f"{query}{operator}{operator_query}"
        query_parameters = urlencode({"q": query, "type": search_type.lower()})
        print(query_parameters)
        return self.base_search(query_parameters)
        
        

