import math
import json

# In a real app, this would be loaded from a geospatial database or a config file
RED_ZONE_POLYGON = [
    (31.0, 77.0), (31.0, 77.01), (31.01, 77.01), (31.01, 77.0)
]

def haversine_meters(lat1, lon1, lat2, lon2):
    R = 6371000
    to_rad = lambda v: (v * math.pi) / 180
    d_lat = to_rad(lat2 - lat1)
    d_lon = to_rad(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(to_rad(lat1)) * math.cos(to_rad(lat2)) * math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def service_check_buffer_zone(tourist_id: int, redis_client):
    """
    Checks if a tourist is near a red zone using the live Redis client.
    """
    print("  [Service] Checking Buffer Zone...")
    log_key = f"tourist:{tourist_id}:logs"
    latest_log_json = redis_client.lindex(log_key, 0)
    if not latest_log_json:
        return {"status": "NO_DATA"}
    
    latest_log = json.loads(latest_log_json)
    lat, lon = latest_log['latitude'], latest_log['longitude']
    
    distances = [haversine_meters(lat, lon, p_lat, p_lon) for p_lat, p_lon in RED_ZONE_POLYGON]
    min_distance = min(distances)
    
    alert_thresholds = {"buffer_100m": 100, "buffer_250m": 250, "buffer_500m": 500}
    
    # Check Redis to see which alerts have already been sent to this user
    sent_alerts_key = f"tourist:{tourist_id}:sent_buffer_alerts"
    
    for alert_key, distance_m in sorted(alert_thresholds.items(), key=lambda item: item[1]):
        if min_distance <= distance_m:
            # hget returns None if field doesn't exist.
            if not redis_client.hget(sent_alerts_key, alert_key):
                print(f"    [ACTION] Tourist crossed {distance_m}m buffer. Sending warning notification.")
                # Mark this alert as sent in Redis, with an expiry to allow re-alerting later
                redis_client.hset(sent_alerts_key, alert_key, "true")
                redis_client.expire(sent_alerts_key, 3600) # Re-arm alerts after 1 hour
                return {"action": "NOTIFY_USER_APP", "reason": f"APPROACHING_RED_ZONE_{distance_m}M"}
            
    return {"status": "OUTSIDE_BUFFER_ZONES"}
