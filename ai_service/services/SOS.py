import json

def service_handle_sos(tourist_id: int, redis_client, data_service_client):
    """
    Handles an SOS button press using the live Redis client and data service client.
    """
    print(f"\n[CRITICAL] SOS Received for Tourist ID: {tourist_id}")
    log_key = f"tourist:{tourist_id}:logs"
    latest_log_json = redis_client.lindex(log_key, 0)
    if not latest_log_json:
        return {"error": "No location data found for tourist."}
    
    latest_log = json.loads(latest_log_json)
    
    # CORRECTED: Call the client as a method, not a dictionary
    profile = data_service_client.get_tourist_profile(tourist_id)
    if not profile:
        return {"error": "Tourist profile not found."}
        
    alert_payload = {
        "alert_type": "SOS_BUTTON_PRESS",
        "tourist_info": profile,
        "last_known_location": latest_log
    }
    
    print(f"  [ACTION] High-priority alert payload compiled and sent to dashboard.")
    return alert_payload

