#!/usr/bin/env python

desc = """
Client tester
"""

from hitcpy import hitcpy
import json

#URL = 'https://morning-meadow-1412.herokuapp.com/'
URL = 'http://localhost:5000/'

if __name__ == "__main__":
    print(desc)
    htm = hitcpy.HITC("http://localhost:5000")
    print ("Making default model")
    model = htm.create_model()
    print "Running data instance 1"
    print model.run({"c0":0,"c1":1})
    print "Resetting"
    print model.reset().json()
    print "Running data instance 2"
    print model.run({"c0":0,"c1":2})

    
    print("Making custom model")
    with open('consumption_model_params.json','r') as f:
        params = json.load(f)
    model2 = htm.create_model(params)
    print model
    print("Running data")
    model2.run({"consumption":50, "timestamp": 1})
    
    
    print("Models are")
    print htm.get_all_models()
    print ("Deleting default model")
    print model2.delete().json()
    print ("Deleting custom model")
    print model.delete().json()
    print("Models are")
    print htm.get_all_models()
