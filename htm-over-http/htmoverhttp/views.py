from pyramid.view import view_config

from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.algorithms import anomaly_likelihood
import json
from uuid import uuid4
from datetime import datetime
import importlib

models = {}
@view_config(route_name='reset', renderer='json')
def reset(request):
    guid = request.matchdict['guid']
    model = models[guid]['model']
    model.resetSequenceStates()
    return {'success':True}

def du(unix):
    return datetime.utcfromtimestamp(unix)
    
@view_config(route_name='run', renderer='json', request_method='GET')
def run(request):
    guid = request.matchdict['guid']
    print guid,'->', request.GET
    data = {k:float(v) for k,v in request.GET.items()}
    # turn the timestamp field into a datetime obj
    data['timestamp'] = du(data['timestamp'])
    model = models[guid]['model']
    result = model.run(data)
    alh = models[guid]['alh']
    pField = models[guid]['pfield']
    anomaly_score = result.inferences["anomalyScore"]
    prediction = result.inferences["multiStepBestPredictions"][1]
    likelihood = alh.anomalyProbability(data[pField], anomaly_score, data['timestamp'])
    return {'likelihood':likelihood, 'prediction':prediction, 'anomaly_score':anomaly_score}

@view_config(route_name='create', renderer='json', request_method='GET')
def create(request):
    predicted_field = request.matchdict['predicted_field']
    guid = str(uuid4())
    params = None
    if not params:
        params = importlib.import_module('model_params.model_params').MODEL_PARAMS
        #print "Using params", json.dumps(params, indent=4)
    model = ModelFactory.create(params)
    model.enableInference({'predictedField': predicted_field})
    models[guid] = {'model':model, 
                    'pfield': predicted_field,
                    'alh': anomaly_likelihood.AnomalyLikelihood(200, 200, reestimationPeriod=10)}
    print "Made model", guid
    return {'guid': guid}
