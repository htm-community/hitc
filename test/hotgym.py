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
def create_model():
    r = requests.get(URL+'create/kw_energy_consumption')
    return r.json()['guid']

def reset_model(model):    
    return requests.get(URL+'reset/'+model).json()

def run_data(model):
    with open('rec-center-hourly.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['timestamp'] = int(time.mktime(datetime.strptime(row['timestamp'], DATE_FORMAT).timetuple()))
            print row
            result = requests.get(URL+'run/'+model, params=row).json()
            print result
    print "Done running"

if __name__ == "__main__":
    print desc
    model = create_model()
    print "Made model", model
    run_data(model)
    print reset_model(model)