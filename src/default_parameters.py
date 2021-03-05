params = {
    "model_params": {"n_estimators": 50, "learning_rate": 0.1},
    "tf_idf_params": {
        "ngram_range": (4, 5),
        "strip_accents": "unicode",
        "analyzer": "char",
        "max_features": 1000,
    },
}
email_col = "email"
pipeline_name = "fraud_model"
target = "label"
