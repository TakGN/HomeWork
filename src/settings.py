import os

DATABASE = {
    'PATH': os.environ.get('DATABASE_PATH'),
}

MODEL = {
    'data_path':  os.environ.get('DATA_PATH'),
    'model_path': os.environ.get('MODEL_PATH'),
    'df_name': os.environ.get('DATASET_NAME'),
}