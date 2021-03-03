from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import pandas as pd

from model import Model
from persistence import TrainModel

app = Flask(__name__)
api = Api(app)


class Prediction(Resource):

    @staticmethod
    def post():
        body = request.json
        query_df = pd.DataFrame(body)
        model = Model.get_model()
        return jsonify({'prediction': model.predict(query_df).tolist(),
                        'prediction_Proba': model.predict_proba(query_df).tolist()})


api.add_resource(Prediction, "/predict")
if __name__ == '__main__':
    app.run(debug=True)
