import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from src.mlProject import logger

STAGE_NAME = "Model Prediction stage"

class PredictionPipeline:
    def __init__(self):
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        self.model = joblib.load(Path('artifacts/model_trainer/model.joblib'))

    def predict(self, data):
        prediction = self.model.predict(data)
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    

        return prediction
    