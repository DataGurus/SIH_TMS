def check_realtime_location(tourist_id: int):
    """
    NEW Primary monitoring function for a single tourist's location update.
    This check has the HIGHEST priority.
    """
    print(f"\n--- [MONITOR] Real-time zone check for Tourist ID: {tourist_id} ---")
    log_key = f"tourist:{tourist_id}:logs"
    if log_key not in mock_redis_db or not mock_redis_db[log_key]:
        return {"status": "NO_DATA"}

    latest_log = mock_redis_db[log_key][-1]
    _timestamp, lat, lon, _speed = latest_log
    current_risk = get_area_risk_score(lat, lon)
    print(f"Current location is in a {current_risk['zone']} zone (Score: {current_risk['score']}).")

    # RULE 1: Immediate Red Zone Alert (Highest Priority)
    if current_risk['zone'] == "RED":
        print("[ACTION] HIGH-PRIORITY: Tourist has entered a RED zone. Escalating to dashboard immediately.")
        return {"action": "ALERT_DASHBOARD", "reason": "RED_ZONE_ENTRY"}
    
    print("[STATUS] Not in a red zone. Other checks can proceed.")
    return {"status": "NOT_IN_RED_ZONE"}