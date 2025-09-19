import os

# Get the base directory of the project, which is the 'ai_service' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Model Configuration ---
# Define the path to the ML model relative to the base directory
MODEL_PATH = os.path.join(BASE_DIR, "services", "best_risk_model_logreg.pkl")

# --- Redis Configuration ---
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
# The Redis channel our app will use to publish alert messages
NOTIFICATION_CHANNEL = "tourist_alerts"

# --- Data Service API (Mock for now) ---
DATA_SERVICE_URL = "http://localhost:8002" 

# --- Safety Logic Thresholds ---
# You can now tune your system's sensitivity from one place.
LOCATION_DROPOFF_THRESHOLD_SECONDS = 300  # 5 minutes
ORANGE_ZONE_NOTIFY_USER_SECONDS = 900     # 15 minutes
ORANGE_ZONE_ESCALATE_SECONDS = 1800     # 30 minutes
INACTIVITY_THRESHOLD_SECONDS = 1800       # 30 minutes
