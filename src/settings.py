import os

DATABASE = {
    'PATH': os.environ.get('DATABASE_PATH'),
}
MODEL = {
    'dataset_path':  os.environ.get('DATASET_PATH'),
    'dataset_name': os.environ.get('DATASET_NAME'),
    'model_path': os.environ.get('MODEL_PATH')
}

