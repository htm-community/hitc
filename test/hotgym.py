#!/usr/bin/env python

import csv
from datetime import datetime
import requests
import time
DATE_FORMAT = "%m/%d/%y %H:%M"
desc = """
Feed the data from rec-center-hourly.csv into the 
htm REST API and compare the results with the 
standard results provided in the tutorial
"""

#URL = 'https://morning-meadow-1412.herokuapp.com/'
URL = 'http://localhost:5000/'


def get(url, params=None):
    return requests.get(URL+url, params=params)


def post(url, params=None):
    return requests.post(URL+url, data=params)


def delete(url):
    return requests.delete(URL+url)


def create_model():
    r = post('models', {'predicted_field': 'kw_energy_consumption'}).json()
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
            result = post('models/run/'+model, row).json()
            print(result)
            c += 1
            if c > 10:
                break
    print("Done running")

if __name__ == "__main__":
    print(desc)
    guid = create_model()
    print("Made model", guid)
    print(get_model(guid).json())
    print("Running data")
    run_data(guid)
    print("Models are")
    print(get_all_models().json())
    print("Resetting model")
    print(reset_model(guid).json())
    print("Deleting model")
    print(delete_model(guid).json())
