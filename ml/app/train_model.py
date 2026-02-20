"""
Model training module extracted from model-ml.py
Handles data loading, preprocessing, and RandomForest model training
"""
import os
import warnings
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV, RepeatedKFold, train_test_split
from sklearn.metrics import r2_score
from joblib import dump, load
from typing import Optional, Tuple

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)

try:
    from alphasense_b_sensors.alphasense_sensors import Alphasense_Sensors
    ALPHASENSE_AVAILABLE = True
except ImportError:
    warnings.warn("alphasense_b_sensors not available")
    ALPHASENSE_AVAILABLE = False


def load_and_preprocess_data(csv_path: str) -> pd.DataFrame:
    """
    Load and preprocess the air quality data from CSV file.
    
    Args:
        csv_path: Path to the CSV file containing the dataset
        
    Returns:
        Preprocessed DataFrame ready for model training
    """
    # Read data
    aqm = pd.read_csv(csv_path)
    
    # Set time index
    aqm.set_index('time', inplace=True)
    aqm.index = pd.to_datetime(aqm.index)
    
    # Define labels and prefix
    labels = ['co_we', 'co_ae', 'temp']
    prefix = ['e2sp_']
    label_ref = 'iag_co'
    
    # Select relevant columns
    df = aqm[[prefix[0] + labels[0], prefix[0] + labels[1], 'pin_umid', 
              label_ref, prefix[0] + 'temp']]
    
    # Resample to 5-minute intervals
    df.index = pd.to_datetime(df.index)
    df = df.resample('5min').mean()
    df = df.interpolate(method='linear', limit=1, limit_area='inside')
    df = df.dropna()
    
    # Calculate CO using Alphasense sensor calibration
    if ALPHASENSE_AVAILABLE:
        co = Alphasense_Sensors("CO-B4", "162741354")
        
        # Convert to mV
        we = df[prefix[0] + labels[0]] * 1000
        ae = df[prefix[0] + labels[1]] * 1000
        
        # Calculate ppb
        ppb = ((we - co.electronic_we) - (ae - co.electronic_ae)) / co.sensitivity
        
        # Convert back to ppm and add to dataframe
        df[prefix[0] + 'co'] = ppb / 1000
    else:
        # Fallback: use a simple calculation if Alphasense is not available
        warnings.warn("Alphasense sensors not available, using simplified CO calculation")
        df[prefix[0] + 'co'] = (df[prefix[0] + labels[0]] - df[prefix[0] + labels[1]]) / 1000
    
    return df


def prepare_training_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepare features (X) and target (y) for model training.
    
    Args:
        df: Preprocessed DataFrame
        
    Returns:
        Tuple of (X, y) where X is features and y is target
    """
    prefix = 'e2sp_'
    label_ref = 'iag_co'
    
    Yco = df[label_ref]
    Xco = df.loc[Yco.index][[
        prefix + 'co', 
        prefix + 'co_we',
        prefix + 'co_ae', 
        prefix + 'temp', 
        'pin_umid'
    ]]
    # Ensure the output is exactly a DataFrame and Series
    Xco = pd.DataFrame(Xco)
    Yco = pd.Series(Yco)
    return Xco, Yco


def train_random_forest_model(
        X_train: pd.DataFrame,
    y_train: pd.Series,
    X_valid: Optional[pd.DataFrame] = None,
    y_valid: Optional[pd.Series] = None,
    verbose: int = 0
) -> GridSearchCV:
    """
    Train a RandomForestRegressor using GridSearchCV.
    
    Args:
        X_train: Training features
        y_train: Training target
        X_valid: Validation features (optional)
        y_valid: Validation target (optional)
        verbose: Verbosity level for GridSearchCV
        
    Returns:
        Trained GridSearchCV object with best estimator
    """
    # Define parameter grid
    param_grid = {
        "randomforestregressor__n_estimators": np.array([32, 64, 124]),
        "randomforestregressor__max_depth": [None, 32],
        "randomforestregressor__bootstrap": [False, True],
        "randomforestregressor__max_features": ["sqrt", None],
        "randomforestregressor__criterion": ['squared_error']
    }
    
    # Create pipeline
    regressor = make_pipeline(RandomForestRegressor())
    
    # Setup cross-validation
    kfold = RepeatedKFold(n_splits=5, n_repeats=1)
    
    # Perform GridSearch
    gs = GridSearchCV(
        regressor,
        param_grid=param_grid,
        n_jobs=-1,
        verbose=verbose,
        return_train_score=True,
        cv=kfold,
        error_score='raise'
    )
    
    #fit the model
    gs.fit(X_train, y_train)
    
    return gs


def train_model_from_csv(
    csv_path: str,
    model_save_path: Optional[str] = None,
    verbose: int = 0
) -> GridSearchCV:
    """
    Complete pipeline: load data, preprocess, and train model.
    
    Args:
        csv_path: Path to the CSV file
        model_save_path: Optional path to save the trained model
        verbose: Verbosity level
        
    Returns:
        Trained GridSearchCV model
    """
    # Load and preprocess data
    df = load_and_preprocess_data(csv_path)
    
    # Prepare training data
    Xco, Yco = prepare_training_data(df)
    
    # Split data
    X_train, X_valid, y_train, y_valid = train_test_split(Xco, Yco, train_size=0.6)
    X_train, X_test, y_train, y_test = train_test_split(X_train, y_train)
    
    # Train model
    gs = train_random_forest_model(X_train, y_train, X_valid, y_valid, verbose=verbose)
    
    # Print training results
    if verbose > 0:
        print("Random Forest Model Training Results:")
        print(f"Train Score: {gs.score(X_train, y_train)}")
        print(f"Test Score: {gs.score(X_test, y_test)}")
        if X_valid is not None and y_valid is not None:
            print(f"Validation Score: {r2_score(y_valid, gs.predict(X_valid))}")
    
    # Save model if path provided
    if model_save_path:
        dump(gs.best_estimator_, model_save_path)
        if verbose > 0:
            print(f"Model saved to {model_save_path}")
    
    return gs


def load_model(model_path: str):
    """
    Load a pre-trained model from file.
    
    Args:
        model_path: Path to the .joblib model file
        
    Returns:
        Loaded model
    """
    return load(model_path)
