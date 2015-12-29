# htm-over-http
temporary name until we decide some things

Chat with us on Gitter:
[![Gitter](https://img.shields.io/badge/gitter-join_chat-blue.svg)](https://gitter.im/nupic-community/htm-over-http?utm_source=badge)

About
=====
This application provides a REST API for use with Nupic. Currently,
it is meant to be deployed on Heroku.

Installation
============

Get a local instance working for testing purposes by cloning this repository
and running `run`. 

Once you've tested it out locally, you can deploy to heroku:

1. Install the heroku toolbelt
2. In the root directory of this project, run `heroku create --stack cedar` 
This will give the git repo a remote repo for heroku
3. Run:
````
 git push heroku master
 heroku scale web=1
 heroku ps # to see if it's running
 heroku logs -t
````

Your API should be ready to go!

API
===
All methods return a JSON response, if a method required a GUID (globally unique identifier), 
and there is no model associated with it, a 404 error will be returned.

While still in development the REST API is as follows:

/models
------

### POST
 
Creates a model, 

##### Parameters

* predicted_field: the field to be predicted
* model_params: the nupic model parameters to be used. If none are provided, default
parameters are provided based on those from the hot gym anomaly detection.

##### Returns

A JSON object containing the GUID of the model and parameters used.

### GET 
 
 
Gets a list of all models and their associated information.

##### Returns

A JSON list of JSON objects containing:

* The GUID of the model
* The parameters used for the mdoel
* The predicted field
* The number of input records processed
* The last input record processed

/models/{guid}
-----------
If the GUID is not found, a 404 error will be returned

### GET

##### Returns

Details of the model


### DELETE

Deletes the model


##### Returns

404 if no such model exists. The body will be a JSON object with:

 * success: true if model was deleted, false otherwise
 * guid: the guid of the model to deleted

/models/run/{guid}
-----------------
Run data through a model

### POST
Run a single record through the model

##### Parameters

All parameters must match those given as the inputs in the parameters

Timestamp must be an integer or float that is a unix timestamp.

##### Returns

Returns the output of the nupic model:

* anomaly score
* prediction
* likelihood

/models/reset/{guid}
-----------------
Resets a model
