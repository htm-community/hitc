#!/usr/bin/env python

desc = """
Class to test the api client

"""

import hitc

#URL = 'https://morning-meadow-1412.herokuapp.com/'
URL = 'http://localhost:5000/'

if __name__ == "__main__":
    print(desc)
    htm = HITC(URL)
    print ("Making default model")
    model = htm.create_model()
    model.reset()
    model.run({})
    model.delete()
    
    
    print("Making custom model")
    model = htm.create_model('consumption_model_params.json')
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
