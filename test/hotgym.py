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

URL = 'https://morning-meadow-1412.herokuapp.com/'

def api(url,params=None):
    return requests.get(url,params).json()
def create_model():
    r = api(URL+'create/kw_energy_consumption')
    return r['guid']

def reset_model(model):    
    return api(URL+'reset/'+model)

def run_data(model):
    with open('rec-center-hourly.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['timestamp'] = int(time.mktime(datetime.strptime(row['timestamp'], DATE_FORMAT).timetuple()))
            print row
            result = api(URL+'run/'+model, row)
            print result
    print "Done running"

if __name__ == "__main__":
    print desc
    model = create_model()
    print "Made model", model
    run_data(model)
    print reset_model(model)
