import os
import pandas as pd


class Dataset:
    def __init__(self, name, path):
        self.name = name
        self.path = os.path.join(path, name)

    def load(self):
        return pd.read_csv(self.path)
