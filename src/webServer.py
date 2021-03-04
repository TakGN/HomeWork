import json
from datetime import datetime

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import pandas as pd

from model import Model
from persistence import TrainModel
from parameters import model_path, pipeline_name, params

app = Flask(__name__)
api = Api(app)


class Prediction(Resource):

    @staticmethod
    def post():
        email = request.json.get('email', '')
        model_name = request.json.get('model_name', pipeline_name)
        query_df = pd.DataFrame([{'email': email}])
        model = Model.load_pipeline(model_path, model_name)
        # Number_requests_processed.inc()
        return jsonify({'prediction for {}'.format(email): model.predict(query_df).tolist(),
                        'model_name': model_name
                        })


class Training(Resource):

    @staticmethod
    def post():
        model_params = request.json.get('model_params')
        model_name = request.json.get('model_name')
        new_model = Model.get_model(model_params, model_name)
        accuracy = new_model[1]
        date = datetime.now().strftime("%m/%d/%Y")
        TrainModel.add(name=model_name,
                       model_params=json.dumps(model_params),
                       accuracy=accuracy,
                       serving=False,
                       train_date=date)
        return '{} is trained successfully'.format(model_name)

    @staticmethod
    def get():
        model = TrainModel.get(id=request.args.get('id', 1))
        return jsonify({'model_name': model.name,
                        'model_accuracy': model.accuracy})


api.add_resource(Prediction, "/predict")
api.add_resource(Training, "/train")

if __name__ == '__main__':
    app.run(debug=True)
