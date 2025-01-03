from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass(frozen=True)
class DataIngestionConfig:
    # Define the fields with type annotations
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    # Define the fields with type annotations
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict

@dataclass(frozen=True)
class DataTransformationConfig:
    # Define the fields with type annotations
    root_dir: Path
    data_path: Path



@dataclass(frozen=True)
class ModelTrainerConfig:
    # Define the fields with type annotations
    root_dir: Path
    train_data_path: Path
    test_data_path: Path   #from confi
    model_name: str     #from config
    random_state: int   #from param
    n_estimators: int   #from param
    target_column: str  #from schema
    selected_features: List[str]


@dataclass(frozen=True)
class ModelEvaluationConfig:
    # Define the fields with type annotations
    root_dir: Path
    test_data_path: Path   #from confi
    model_path: Path    #from config
    all_params: dict
    metric_file_name: Path
    target_column: str
    selected_features: List[str]
