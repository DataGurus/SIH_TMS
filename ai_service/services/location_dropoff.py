import time
import json
from config import (
    LOCATION_DROPOFF_THRESHOLD_SECONDS,
    ORANGE_ZONE_NOTIFY_USER_SECONDS,
    ORANGE_ZONE_ESCALATE_SECONDS
)

def service_check_location_dropoff(tourist_id: int, redis_client):
    """
    Final, self-sufficient version. Fetches the last known log from Redis
    and uses the risk score that was already stored with it.
    """
    print("  [Service] Checking Location Dropoff...")
    log_key = f"tourist:{tourist_id}:logs"
    latest_log_json = redis_client.lindex(log_key, 0)
    if not latest_log_json:
        return {"status": "NO_DATA"}
        
    latest_log = json.loads(latest_log_json)
    time_since_last_signal = time.time() - latest_log["timestamp"]
    
    if time_since_last_signal <= LOCATION_DROPOFF_THRESHOLD_SECONDS:
        return {"status": "ACTIVE"}

    last_known_risk = latest_log["risk_score_result"]
    
    if last_known_risk['zone'] in ["GREEN", "YELLOW"]:
        return {"action": "NO_ACTION", "reason": "Signal lost in low-risk zone."}

    if last_known_risk['zone'] == "ORANGE":
        if time_since_last_signal >= ORANGE_ZONE_ESCALATE_SECONDS:
            return {"action": "ALERT_DASHBOARD", "reason": "Signal lost in Orange zone after prolonged wait."}
        elif time_since_last_signal >= ORANGE_ZONE_NOTIFY_USER_SECONDS:
            return {"action": "NOTIFY_USER_APP", "reason": "Signal lost in Orange zone, checking if user is okay."}
        else:
            return {"status": "SIGNAL_LOST_WAITING"}
            
    return {"status": "UNHANDLED"}
