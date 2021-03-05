
default_model_params = {
    "model_params": {
        "n_estimators": 50, "learning_rate": 0.1
    }
}
default_processor_params = {
    "tf_idf_params": {
        "ngram_range": (4, 5),
        "strip_accents": "unicode",
        "analyzer": "char",
        "max_features": 1000,
    }

}
pipeline_name = "fraud_model"
