import requests
import json

def put(url, params=None):
    return requests.put(URL+url, data=params)

    
def get(url, params=None):
    return requests.get(URL+url, params=params)


def post(url, params=None):
    return requests.post(URL+url, data=params)


def delete(url):
    return requests.delete(URL+url)


class HITC(object):
    def __init__(self, url):
        self.url = url
        
        
    def create_model(model_params=None):
        r = post('models', json.dumps(model_params))
        return Model(r, self.url)


    def get_model(self, model):
        return Model(get('models/'+model), self.url)


    def get_all_models():
        return [Model(m, url) for m in  get('models')]

    
class Model(object):
    def __init__(self, req):
        print req
        if req.status_code in [400, 404, 500]:
            raise ValueError(req.reason)
        req = req.json()
        self.guid = req['guid']
        self.params = req['params']
        self.info = req['info']
        self.predicted_field = req['predicted_field']
        self.seen = 0
        self.last = None
        self.deleted = False
        
    def reset(self, model):    
        return get(self.url+'models/reset/'+self.guid)


    def delete(model):
        self.deleted = True
        return delete(self.url+'models/'+self.guid)
        
        
    def run(self, row):
        r = put(self.url+'models/'+self.guid, json.dumps(row))
        if r.status_code == 400:
            raise ValueError(req.reason)
            return None
        else:
            r = r.json()
            self.seen = r['seen']
            self.last = r['last']
            return r
        
