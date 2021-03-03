from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import pandas as pd

from model import Model
from persistence import TrainModel
from parameters import model_path, pipeline_name

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

    def post(self):
        body = request.json
        query_df = pd.DataFrame(body)
        model = Model.get_model()
        return jsonify({'prediction': model.predict(query_df).tolist(),
                        'prediction_Proba': model.predict_proba(query_df).tolist()})


api.add_resource(Prediction, "/predict")
if __name__ == '__main__':
    app.run(debug=True)
