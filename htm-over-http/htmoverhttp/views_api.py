from pyramid.view import view_config
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.algorithms import anomaly_likelihood
from uuid import uuid4
from datetime import datetime
import importlib
from copy import copy

models = {}


@view_config(route_name='reset', renderer='json')
def reset(request):
    guid = request.matchdict['guid']
    has_model = guid in models
    if has_model:
        print "resetting model", guid
        models[guid]['model'].resetSequenceStates()
        models[guid]['seen'] = 0
        models[guid]['last'] = None
        models[guid]['alh'] = anomaly_likelihood.AnomalyLikelihood()
    else:
        request.response.status = 404
    return {'success': has_model, 'guid': guid}


def du(unix):
    return datetime.utcfromtimestamp(float(unix))


@view_config(route_name='run', renderer='json', request_method='POST')
def run(request):
    guid = request.matchdict['guid']
    has_model = guid in models
    if not has_model:
        request.response.status = 404
        return {}
    models[guid]['seen'] += 1
    print guid, '<-', request.POST
    data = {k: float(v) for k, v in request.POST.items()}
    models[guid]['last'] = copy(data)
    # turn the timestamp field into a datetime obj
    data['timestamp'] = du(data['timestamp'])
    model = models[guid]['model']
    result = model.run(data)
    alh = models[guid]['alh']
    predicted_field = models[guid]['pfield']
    anomaly_score = result.inferences["anomalyScore"]
    prediction = result.inferences["multiStepBestPredictions"][1]
    likelihood = alh.anomalyProbability(data[predicted_field], anomaly_score, data['timestamp'])
    
    return {'likelihood': likelihood, 'prediction': prediction, 'anomaly_score': anomaly_score}


@view_config(route_name='models', renderer='json', request_method='DELETE')
def model_delete(request):
    guid = request.matchdict['guid']
    has_model = guid in models
    if not has_model:
        request.response.status = 404
    else:
        print "Deleting model", guid
        del models[guid]
    return {'success': has_model, 'guid': guid}


@view_config(route_name='models', renderer='json', request_method='GET')
def model_get(request):
    guid = request.matchdict['guid']
    has_model = guid in models
    if not has_model:
        request.response.status = 404
        return {}
    else:
        return serialize_model(guid)


def serialize_model(guid):
    data = models[guid]
    return {
        'guid': guid,
        'predicted_field': data['pfield'],
        'params': data['params'],
        'last': data['last'],
        'seen': data['seen']
    }


@view_config(route_name='model_create', renderer='json', request_method='GET')
def model_list(request):
    return [serialize_model(guid) for guid in models]


@view_config(route_name='model_create', renderer='json', request_method='POST')
def model_create(request):
    predicted_field = request.POST['predicted_field']
    guid = str(uuid4())
    params = request.POST.get('model_params', None)
    if not params:
        params = importlib.import_module('model_params.model_params').MODEL_PARAMS
        # print "Using params", json.dumps(params, indent=4)
    model = ModelFactory.create(params)
    model.enableInference({'predictedField': predicted_field})
    models[guid] = {'model': model,
                    'pfield': predicted_field,
                    'params': params,
                    'seen': 0,
                    'last': None,
                    'alh': anomaly_likelihood.AnomalyLikelihood()}
    print "Made model", guid
    return {'guid': guid, 'params': params}
