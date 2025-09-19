import json

def service_compile_efir_data(tourist_id: int, incident_details: dict, redis_client, data_service_client):
    """
    Aggregates data for an E-FIR package using live Redis and the data service client.
    """
    print(f"\n[INFO] Compiling E-FIR data package for Tourist ID: {tourist_id}")
    
    # CORRECTED: Call the client as a method, not a dictionary
    tourist_profile = data_service_client.get_tourist_profile(tourist_id)
    if not tourist_profile:
        return {"error": "Tourist profile not found"}
        
    log_key = f"tourist:{tourist_id}:logs"
    location_trail_json = redis_client.lrange(log_key, 0, -1)
    location_trail = [json.loads(log) for log in location_trail_json]
    
    efir_package = {
        "incident_details": incident_details,
        "tourist_profile": tourist_profile,
        "location_trail": location_trail
    }
    
    print("  [SUCCESS] E-FIR data package compiled.")
    return efir_package

