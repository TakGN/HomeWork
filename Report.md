# Report on the Technical Test
This report documents, explains and answers the questions 
on the task provided by Deezer data science team.

##Comments on the code 

I have chosen to layout my code as follows:

- web_server.py: the web server running on Flask and implementing all this exercise endpoints.
- persistence.py: the database layer running with SQLAlchemy for sqlite database 
  and handles some basic database operations.
- tests_web_server.py: it implements the unit tests for the HTTP requests for our endpoints.
- setting.py: includes the general setting for our app such as the database path.
- export.sh: exports all variables in settings as env variables.
- model.py: has the model and basically is a refactor of the notebooks.

I have implemented exception handling for all four endpoints 

##API creation

To provide an endpoint to server the fraud detection model, 
[**Flask**](https://flask.palletsprojects.com/en/1.1.x/) framework is chosen as a web server. 
Flask is chosen because it is light weight and written 
in Python which would make integrating the model written in Python itself easier. 
### web server
ththe web server implementation in the code for this exercise has two endpoints: 

####class Predictions (/predict):

In this endpoint the post method (HTTP POST) is implemented and would retrieve en email and model name 
provided by the user and returns a prediction for the given email by that given model.

**example**

```sh

POST /predict
{
    "email": "takwa.gnenna@gmail.com",
    "model_name": "wonderful_model"

   }
```

_which would return_

```sh
{
    "model_name": "fraud_model",
    "prediction for takwa.gnenna@DSDF.com": [
        1
    ]
}
```


####class Training (/train):

Three methods are provided:

the post method would allow a user to train a model providing new parameters.

**example**

```sh

POST /train
{
    "model_name" : "fantastic_model",
    "model_type" : "GradientBoosting",
    "model_params" :  {
        "model_params": {"n_estimators": 50, "learning_rate": 0.1},
        "tf_idf_params": {
            "ngram_range": [4, 5],
            "strip_accents": "unicode",
            "analyzer": "char",
            "max_features": 1000
        }
    }  
}
```

__it would return__

```sh
{
    "accuracy": 0.8885,
    "id": 4,
    "model_params": {
        "model_params": {
            "learning_rate": 0.1,
            "n_estimators": 50
        },
        "tf_idf_params": {
            "analyzer": "char",
            "max_features": 1000,
            "ngram_range": [
                4,
                5
            ],
            "strip_accents": "unicode"
        }
    },
    "name": "fantastic",
    "serving": false,
    "train_date": "Fri, 05 Mar 2021 10:31:59 GMT"
}
```


The get methods would allow to see:

#####a specific models 

```sh
GET /train?id=1

```

__it would return information on model number 5__

```sh
{
    "accuracy": 0.888,
    "id": 1,
    "model_params": {
        "model_params": {
            "learning_rate": 0.1,
            "n_estimators": 50
        },
        "tf_idf_params": {
            "analyzer": "char",
            "max_features": 1000,
            "ngram_range": [
                4,
                5
            ],
            "strip_accents": "unicode"
        }
    },
    "name": "cx",
    "serving": false,
    "train_date": "Thu, 04 Mar 2021 23:30:28 GMT"
}
```

#####all models 
```sh
GET /train

```
__would return a list of all models and their information in the database__

And finally a put method which would allow to change a serving status of a certain model of our choice.

```sh
PUT /train

{   "id": 4,
    "serving": true 
}

```

it would change the serving status of model 4 and would return


```sh
{
    "accuracy": 0.8885,
    "id": 4,
    "model_params": {
        "model_params": {
            "learning_rate": 0.1,
            "n_estimators": 50
        },
        "tf_idf_params": {
            "analyzer": "char",
            "max_features": 1000,
            "ngram_range": [
                4,
                5
            ],
            "strip_accents": "unicode"
        }
    },
    "name": "fantastic",
    "serving": true,
    "train_date": "Fri, 05 Mar 2021 10:31:59 GMT"
}
```

we can see which model is on use by looking at the serving status of all models. 


### database operations

**Sqlite** database is used to store the different models’ meta-data: name, date of creation, accuracy,...
Flask does not have database abstraction layer, so an extension is used that is **sqlalchemy** to handle the database operations. 
Only basic operations are implemented during this exercise: 

**add**: to add a model to the database
**get**: to get a model by id
**query**: to get all models in the database 

##API monitoring 

For monitoring the API the choice was [**prometheus**](https://prometheus.io/)
which is an open source monitoring system with a times series database 
which means you can see metrics and their evolution through time easily.
To monitor the total number of predictions, a counter is created which is a prometheus data metric
and will be incremented for evert call to our (/predict) endpoint.
To monitor the total number of fraud predictions, another counter is created and would be only incremented in case of 
a fraud detection.

the **python prometheus_client** was used to implement the counter 
and the **prometheus_flask_exporter** was used to export the metrics to the default endpoint (metrics).

``` python 

total_predictions = Counter('predictions',
                            'Total number of predictions',
                            ['model_name'])
                            
total_fraud_predictions = Counter('fraud_predictions',
                                  'Total number of fraud_predictions')
```
An instance of prometheus needs to be running on your system to scrape the metrics. 
A docker image of prometheus is used with a basic configuration.
