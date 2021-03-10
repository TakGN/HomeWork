import os

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import logging
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, path, model_name, model_kwargs=None,
                 processor_kwargs=None):
        self.path = os.path.join(path, model_name)
        self.feature_name = "email"
        self.target_name = "label"

        if model_kwargs is None and processor_kwargs is None:
            self.pipeline = self.load()
            self.model = self.pipeline['model']
            self.processor = self.pipeline['model']
        else:
            self.model = GradientBoostingClassifier(**model_kwargs)
            self.processor = ColumnTransformer([("email_transformer",
                                                 TfidfVectorizer(**processor_kwargs),
                                                 self.feature_name)])
            self.pipeline = Pipeline([("preprocessing", self.processor),
                                      ("model", self.model)])

    def fit(self, data, **kwargs):

        train_df, test_df = train_test_split(data, test_size=0.2)

        self.pipeline.fit(train_df[[self.feature_name]],
                          train_df[[self.target_name]],
                          **kwargs)
        score = self.accuracy(test_df[[self.feature_name]],
                              test_df[[self.target_name]])
        self.save()
        return score

    def predict(self, x):
        return self.pipeline.predict(x)

    def save(self):

        joblib.dump(self.pipeline, self.path)

    def load(self):
        return joblib.load(self.path)

    def accuracy(self, x, y):
        predictions = self.pipeline.predict(x)
        score = accuracy_score(predictions, y)
        return score







