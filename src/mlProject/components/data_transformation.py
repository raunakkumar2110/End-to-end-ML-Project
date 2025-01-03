import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
import logging
from imblearn.over_sampling import SMOTE

# Assuming logger is set up
logger = logging.getLogger(__name__)

class DataTransformation:
    def __init__(self, config):
        self.config = config

    ## Log Transformation Method
    def log_transform(self, column_names):
        """
        Applies log transformation to specified column(s) in the data.
        Args:
            column_names (str or list): The column(s) to apply the log transformation on.
        """
        data = pd.read_csv(self.config.data_path)

        # If a single column name is passed (string), convert it to a list
        if isinstance(column_names, str):
            column_names = [column_names]

        # Apply log transformation to each specified column
        for column_name in column_names:
            if column_name in data.columns:
                data[column_name] = np.log1p(data[column_name])  # log1p applies log(x + 1)
                logger.info(f"Applied log transformation on column: {column_name}")
            else:
                logger.warning(f"Column {column_name} not found in the dataset.")
        
        return data

    ## Outlier Removal Method
    def remove_outliers(self, df, columns):
        """
        Removes outliers from the specified columns using the IQR method.
        Args:
            df (pd.DataFrame): The dataset.
            columns (list): List of column names to check for outliers.
        """
        for column in columns:
            Q1 = df[column].quantile(0.25)  # First quartile (25th percentile)
            Q3 = df[column].quantile(0.75)  # Third quartile (75th percentile)
            IQR = Q3 - Q1                   # Interquartile range

            # Define the outlier boundaries
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Remove outliers
            df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
            logger.info(f"Outliers removed from column: {column}")

        return df

    ## Preprocessing Method that combines log transformation, outlier removal, and train-test split
    def preprocess(self):
        # Step 1: Load data
        data = pd.read_csv(self.config.data_path)

        # Step 2: Apply log transformation to specified columns
        columns_to_transform = ['BMI']  # Replace with your columns to apply log transformation
        data = self.log_transform(columns_to_transform)

        # Step 3: Remove outliers from specified columns after log transformation
        columns_to_check_for_outliers = ['BMI', 'GenHlth', 'PhysHlth', 'MentHlth']  # Replace with your columns
        data = self.remove_outliers(data, columns_to_check_for_outliers)

        # Step 4: Separate features and target variable
        target_column = 'Diabetes_012'  # Replace with your target column
        if target_column not in data.columns:
            raise ValueError(f"Target column {target_column} not found in the dataset")

        X = data.drop(columns=[target_column])
        y = data[target_column]

        # Step 3: Split into training and testing sets (before applying SMOTE)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )

        # Step 4: Print class frequency before resampling (in the training set)
        print("\nClass frequency in data before resampling:")
        print(y.value_counts())
        logger.info(f"Class frequency in data before resampling: {y.value_counts().to_dict()}")

        # Step 5: Apply SMOTE only on the training data
        smote = SMOTE(random_state=42)
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

        # Step 6: Print class frequency after resampling
        print("\nClass frequency in training set after resampling:")
        print(pd.Series(y_train_resampled).value_counts())
        logger.info(f"Class frequency in training set after resampling: {pd.Series(y_train_resampled).value_counts().to_dict()}")

        # Step 7: Combine features and target for saving
        train = pd.concat([X_train_resampled, y_train_resampled], axis=1)
        test = pd.concat([X_test, y_test], axis=1)

        # Step 8: Save train and test datasets
        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)

        logger.info("Split data into training and test sets after applying SMOTE to the training set only")
        logger.info("Data")
        logger.info("SMOTE Applied Successfully:")
        
        logger.info(f"Train shape: {train.shape}")
        logger.info(f"Test shape: {test.shape}")

        print("\nTraining and testing datasets saved.")
        print(f"Train shape: {train.shape}")
        print(f"Test shape: {test.shape}")