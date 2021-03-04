import json
from datetime import datetime

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from prometheus_client import Counter
import pandas as pd
from prometheus_flask_exporter import PrometheusMetrics

from model import Model
from persistence import TrainModel
from parameters import model_path, pipeline_name, params

total_predictions = Counter('predictions',
                            'Total number of predictions',
                            ['model_name', 'date'])
total_fraud_predictions = Counter('fraud_predictions',
                                  'Total number of fraud_predictions')

app = Flask(__name__)
api = Api(app)
metrics = PrometheusMetrics(app)


class Prediction(Resource):

    @staticmethod
    def post():
        email = request.json.get('email', '')
        model_name = request.json.get('model_name', pipeline_name)
        query_df = pd.DataFrame([{'email': email}])
        model = Model.load_pipeline(model_path, model_name)
        prediction = model.predict(query_df).tolist()
        labels = {'model_name': model_name,
                  'date': datetime.now().strftime("%m/%d/%Y")}
        if prediction[0]:
            total_fraud_predictions.inc()

        total_predictions.labels(**labels).inc()
        return jsonify({'prediction for {}'.format(email): prediction,
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
        new_model = TrainModel.add(name=model_name,
                                   model_params=json.dumps(model_params),
                                   accuracy=accuracy,
                                   serving=False,
                                   train_date=date)
        return jsonify(new_model.dict())

    @staticmethod
    def get():
        if request.args.get('id', ''):
            model = TrainModel.get(id=request.args.get('id', 1))
            return jsonify(model.dict())
        else:
            models = TrainModel.query()
            all_models = []
            for model in models:
                all_models.append(model.dict())

            return jsonify(all_models)

    @staticmethod
    def put():
        body = request.json
        model_id = request.args.get('id', '')
        edited_model = TrainModel.edit(id=model_id, **body)
        return jsonify(edited_model.dict())


api.add_resource(Prediction, "/predict")
api.add_resource(Training, "/train")

if __name__ == '__main__':
    app.run(debug=False)
