import joblib
import pandas as pd
import numpy as np
from config import MODEL_PATH

# Load the model once when the service starts
try:
    loaded_model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    print(f"CRITICAL ERROR: ML Model not found at path: {MODEL_PATH}")
    print("The application cannot start without the model file.")
    # In a real app, you might fall back to a default or exit. For now, we create a mock.
    loaded_model = None

def service_calculate_risk_score(latitude: float, longitude: float) -> dict:
    """
    Generates a risk score for a given location.
    Uses the loaded ML model.
    """
    # This is a placeholder for how you'd convert lat/lon to your model's features
    # e.g., using a reverse geocoder or a k-d tree to find the nearest locality name.
    # For now, we'll use a mock based on the loaded model if available.
    
    if loaded_model:
        # MOCK FEATURE ENGINEERING
        # In a real system, you would convert lat/lon to 'locality_name' and 'time_of_day'
        locality_name_mock = "Girahapa_Area_0" 
        time_of_day_mock = "EVENING"

        new_sample = pd.DataFrame({
            "locality_name": [locality_name_mock],
            "time_of_day": [time_of_day_mock]
        })

        pred_label = loaded_model.predict(new_sample)[0]
        pred_proba = loaded_model.predict_proba(new_sample)[0]
        class_labels = loaded_model.named_steps["model"].classes_
        pred_index = list(class_labels).index(pred_label)
        pred_score = pred_proba[pred_index]

        # Assuming your labels are "Safe", "Moderate", "Risky" which map to GREEN, YELLOW, ORANGE
        zone_map = {"Safe": "GREEN", "Moderate": "YELLOW", "Risky": "ORANGE"}
        zone = zone_map.get(pred_label, "UNKNOWN")
        
        return {"score": round(pred_score * 10, 2), "zone": zone}
    else:
        # Fallback if model loading failed
        if latitude > 25: return {"score": 6.5, "zone": "ORANGE"}
        if latitude > 18.8: return {"score": 4.5, "zone": "YELLOW"}
        return {"score": 1.5, "zone": "GREEN"}
