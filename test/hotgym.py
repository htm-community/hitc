#!/usr/bin/env python

import csv
from datetime import datetime
import requests
import time
import json
import sys

DATE_FORMAT = "%m/%d/%y %H:%M"
desc = """
Feed the data from rec-center-hourly.csv into the 
htm REST API and compare the results with the 
standard results provided in the tutorial
"""

URL = 'https://morning-meadow-1412.herokuapp.com/'
#URL = 'http://localhost:5000/'


def put(url, params=None):
    return requests.put(URL+url, data=params)

    
def get(url, params=None):
    return requests.get(URL+url, params=params)


def post(url, params=None):
    return requests.post(URL+url, data=params)


def delete(url):
    return requests.delete(URL+url)


def create_model(model_params=None):
    opts = {'predicted_field': 'kw_energy_consumption'}
    if model_params:
        with open(model_params) as data_file:
            opts['model_params'] = json.dumps(json.load(data_file))
    r = post('models', opts).json()
    return r['guid']


def reset_model(model):    
    return get('models/reset/'+model)


def delete_model(model):
    return delete('models/'+model)


def get_model(model):
    return get('models/'+model)


def get_all_models():
    return get('models')


def run_data(model):
    with open('rec-center-hourly.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        c = 0
        for row in reader:
            row['timestamp'] = int(time.mktime(datetime.strptime(row['timestamp'], DATE_FORMAT).timetuple()))
            print(row)
            result = put('models/'+model, json.dumps(row)).json()
            #print(result)
            c += 1
            if c > 10:
                break
    #check that we can't insert any old data
    print("checking we can't run old data")
    print(put('models/'+model, {'timestamp': 1, 'kw_energy_consumption': 5}).json())
    print("Done running")

if __name__ == "__main__":
    print(desc)
    print ("Making model from json")
    custom_model = create_model('model_params.json')
    print ("Deleting custom model")
    print(delete_model(custom_model))
    print("Making default model")
    guid = create_model('hot_gym_params.json')
    print("Made default model", guid)
    print(get_model(guid).json())
    print("Running data")
    run_data(guid)
    print("Models are")
    print(get_all_models().json())
    print("Resetting model")
    print(reset_model(guid).json())
    print("Deleting model")
    print(delete_model(guid).json())
