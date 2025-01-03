import os
from src.mlProject import logger
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
from src.mlProject.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        # Load data
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        # Get selected features and target column from the config
        selected_features = self.config.selected_features
        target_column = self.config.target_column
        logger.info("Features Successfully Selected")

        # Ensure that the selected features are present in the data
        for feature in selected_features:
            if feature not in train_data.columns:
                raise ValueError(f"Feature column '{feature}' not found in the dataset")

        # Prepare train and test data (select only the defined feature columns)
        train_x = train_data[selected_features]
        test_x = test_data[selected_features]
        train_y = train_data[target_column]
        test_y = test_data[target_column]

        # Train the model (Random Forest in this case)
        rf = RandomForestClassifier(random_state=self.config.random_state, n_estimators=self.config.n_estimators)
        rf.fit(train_x, train_y)

        # Save the trained model
        # joblib.dump(rf, os.path.join(self.config.root_dir, self.config.model_name),compress=("zlib",9))   #here aadded code for compression
        joblib.dump(rf, os.path.join(self.config.root_dir, self.config.model_name))