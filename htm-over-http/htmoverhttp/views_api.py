import json
from pyramid.view import view_config
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.algorithms import anomaly_likelihood
from uuid import uuid4
from datetime import datetime
import time
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
        return no_model_error()
    return {'success': has_model, 'guid': guid}


def du(unix):
    return datetime.utcfromtimestamp(float(unix))


def dt_to_unix(dt):
    return int(time.mktime(datetime.now().timetuple()))


def no_model_error():
    return {'error': 'No such model'}


def serialize_result(result):
    result.rawInput['timestamp'] = dt_to_unix(result.rawInput['timestamp'])
    out = dict(
        predictionNumber=result.predictionNumber,
        rawInput=result.rawInput,
        sensorInput=dict(
            dataRow=result.sensorInput.dataRow,
            dataDict=result.rawInput,
            dataEncodings=[map(int, list(l)) for l in result.sensorInput.dataEncodings],
            sequenceReset=int(result.sensorInput.sequenceReset),
            category=result.sensorInput.category
        ),
        inferences=result.inferences,
        metrics=result.metrics,
        predictedFieldIdx=result.predictedFieldIdx,
        predictedFieldName=result.predictedFieldName,
        classifierInput=dict(
            dataRow=result.classifierInput.dataRow,
            bucketIndex=result.classifierInput.bucketIndex
        )
    )
    return out


@view_config(route_name='models', renderer='json', request_method='PUT')
def run(request):
    guid = request.matchdict['guid']
    has_model = guid in models
    if not has_model:
        request.response.status = 404
        return no_model_error()
    print guid, '<-', request.json_body
    data = {k: float(v) for k, v in request.json_body}
    if models[guid]['last'] and (data['timestamp'] < models[guid]['last']['timestamp']):
        request.response.status = 400
        return {'error': 'Cannot run old data'}
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
    models[guid]['seen'] += 1
    return {'likelihood': likelihood,
            'prediction': prediction,
            'anomaly_score': anomaly_score,
            'model_result': serialize_result(copy(result))
    }


@view_config(route_name='models', renderer='json', request_method='DELETE')
def model_delete(request):
    guid = request.matchdict['guid']
    has_model = guid in models
    if not has_model:
        request.response.status = 404
        return no_model_error()
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
        return no_model_error()
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
    guid = str(uuid4())
    predicted_field = request.POST.get('predicted_field', None)
    params = json.loads(request.POST.get('model_params', 'false'))
    msg = ''
    if params:
        if 'predictedField' in params:
            predicted_field = params['predictedField']
        params = params['modelParams']
    else:
        params = importlib.import_module('model_params.model_params').MODEL_PARAMS['modelConfig']
        msg = 'Using default parameters, timestamp is field c0 and input and predictedField is c1'
        predicted_field = 'c1'
        # no predictedField is given here...
    if not predicted_field:
        request.response.status = 500
        return {'error': 'Please provide a predicted_field either as a ' +
                         'POST param or in the model_params as predictedField'}
    model = ModelFactory.create(params)
    if predicted_field:
        model.enableInference({'predictedField': predicted_field})
    models[guid] = {'model': model,
                    'pfield': predicted_field,
                    'params': params,
                    'seen': 0,
                    'last': None,
                    'alh': anomaly_likelihood.AnomalyLikelihood()}
    print "Made model", guid
    return {'guid': guid, 'params': params, 'predicted_field': predicted_field, 'msg': msg}
