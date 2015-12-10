#!/usr/bin/env python
import requests
import json
from pprint import pprint
DATE_FORMAT = "%m/%d/%y %H:%M"
desc = """
A test the shows created models do not return the right field names.
"""

URL = 'http://localhost:5000/'


def post(url, data=None):
    return requests.post(URL+url, data=data)

def get(url, params=None):
    return requests.get(URL+url, params=params)

def create_model(model_params):
    with open(model_params) as data_file:
        opts = json.dumps(json.load(data_file))
    r = post('models', opts)
    r.raise_for_status()
    print r
    return r.json()['guid']

def get_model(model):
    return get('models/'+model)

if __name__ == "__main__":
    
    print(desc)
    print ("Making prediction model from model_params.json")
    custom_model = create_model('consumption_model_params.json')
    pprint (get_model(custom_model).json())
