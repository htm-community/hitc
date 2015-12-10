#!/usr/bin/env python
import csv
from datetime import datetime
import requests
import time
import json
import sys

DATE_FORMAT = "%m/%d/%y %H:%M"
desc = """
A test the shows created models do not return the right field names.
"""

URL = 'http://localhost:5000/'


def post(url, params=None):
    return requests.post(URL+url, data=params)

def get(url, params=None):
    return requests.get(URL+url, params=params)

def put(url, params=None):
    return requests.put(URL+url, data=params)

def create_model(model_spec):
    response = post('models', model_spec)
    r = response.json()
    if response.status_code == 200:
        return r['guid']
    else:
        raise Exception("Could not create model: " + r['error'])

def get_model(model):
    return get('models/'+model)

def run_data(model, fieldname="kw_energy_consumption"):
    with open('rec-center-hourly.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        c = 0
        for row in reader:
            row['timestamp'] = int(time.mktime(datetime.strptime(row['timestamp'], DATE_FORMAT).timetuple()))
            if fieldname is not "kw_energy_consumption":
                row[fieldname] = row["kw_energy_consumption"]
                del row["kw_energy_consumption"]
            print(row)
            result = put('models/'+model, json.dumps(row)).json()
            #print(result)
            c += 1
            if c > 10:
                break
    #check that we can't insert any old data
    print("checking we can't run old data")
    print(put('models/'+model, json.dumps({'timestamp': 1, fieldname: 5})).json())
    print("Done running")



if __name__ == "__main__":
    from pprint import pprint
    print(desc)
    print ("Making prediction model from model_params.json")
    with open('model_params.json') as data_file:
        model_spec = data_file.read()
    custom_model = create_model(model_spec)
    # custom_model = create_model(model_spec)
    pprint (get_model(custom_model).json())
    run_data(custom_model, fieldname="consumption")
