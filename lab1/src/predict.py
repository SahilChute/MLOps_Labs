import joblib
import numpy as np

MODEL_PATH = "../model/breast_cancer_model.pkl"

# Load the model ONCE when the module is imported
try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

def predict_data(X):
    """
    X: list or numpy array of shape (1, n_features)
    """
    if model is None:
        raise ValueError("Model not loaded")
    
    X = np.array(X)
    return model.predict(X)