import time
import json
from config import INACTIVITY_THRESHOLD_SECONDS

def service_check_inactivity(tourist_id: int, redis_client):
    """
    Final, self-sufficient version. Fetches recent logs and the current risk
    score from the latest log in Redis to make its decision.
    """
    print("  [Service] Checking Inactivity...")
    log_key = f"tourist:{tourist_id}:logs"
    
    # Fetch a sample of recent logs to check for movement
    recent_logs_json = redis_client.lrange(log_key, 0, 10) 
    if not recent_logs_json:
        return {"status": "NO_DATA"}
        
    recent_logs = [json.loads(log) for log in recent_logs_json]
    
    # Check if the tourist is moving based on the most recent logs
    is_stationary = all(log.get("speed_kmh", 0.0) == 0.0 for log in recent_logs)
    if not is_stationary:
        return {"status": "ACTIVE"}

    # --- THE CRITICAL FIX ---
    # If stationary, check for how long based on the OLDEST log in our full history.
    # To do this robustly, we find the log with the minimum timestamp.
    full_history_json = redis_client.lrange(log_key, 0, -1)
    full_history = [json.loads(log) for log in full_history_json]
    
    # Find the log with the smallest (oldest) timestamp
    oldest_log = min(full_history, key=lambda log: log["timestamp"])
    duration_of_inactivity = time.time() - oldest_log["timestamp"]

    if duration_of_inactivity < INACTIVITY_THRESHOLD_SECONDS:
        return {"status": "INACTIVE_WAITING"}
    
    # If the threshold is passed, escalate based on the risk of the CURRENT stationary location
    # The current risk is in the most recent log (the first item in the list)
    current_risk = recent_logs[0]["risk_score_result"]

    if current_risk['zone'] == "ORANGE":
        return {"action": "ALERT_DASHBOARD", "reason": "Prolonged inactivity in a high-risk (Orange) zone."}
    else: # GREEN or YELLOW zone
        return {"action": "ALERT_NEARBY_TOURISTS", "reason": "Prolonged inactivity in a low-risk zone."}

