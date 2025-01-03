import pandas as pd
import joblib
import os
from sklearn.metrics import accuracy_score
import numpy as np
from urllib.parse import urlparse
from src.mlProject.utils.common import save_json
from src.mlProject.entity.config_entity import ModelEvaluationConfig
from pathlib import Path

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
    
    def eval_metrics(self,actual, pred):
        acc = accuracy_score(actual, pred)
        return acc
        
    def save_results(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data[self.config.selected_features]
        test_y = test_data[[self.config.target_column]]
        
        predicted_qualities = model.predict(test_x)

        acc = self.eval_metrics(test_y, predicted_qualities)
        
        # Saving metrics as local
        scores = {"Accuracy": acc}
        save_json(path=Path(self.config.metric_file_name), data=scores)
