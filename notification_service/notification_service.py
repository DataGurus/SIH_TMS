import redis
import json
import time

# --- Configuration ---
# In a real production system, this would be loaded from a shared config
# or environment variables, just like in your ai_service.
REDIS_HOST = "localhost"
REDIS_PORT = 6379
NOTIFICATION_CHANNEL = "tourist_alerts"

def main():
    """
    A simple, standalone service that subscribes to the Redis alert channel
    and dispatches notifications based on the message content.
    This is the "mouth" of the system.
    """
    print("--- Notification Service Started ---")
    
    while True: # Add a loop to attempt reconnection if Redis isn't ready
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
            pubsub = r.pubsub()
            pubsub.subscribe(NOTIFICATION_CHANNEL)
            print(f"Successfully subscribed to channel: '{NOTIFICATION_CHANNEL}'")
            break # Exit loop if connection succeeds
        except redis.exceptions.ConnectionError:
            print("Could not connect to Redis. Retrying in 5 seconds...")
            time.sleep(5)

    # Listen for messages indefinitely
    for message in pubsub.listen():
        if message['type'] == 'message':
            # Decode the message data from bytes to a string, then parse JSON
            data = json.loads(message['data'].decode('utf-8'))
            
            print("\n----------------------------------------")
            print(f"RECEIVED ALERT at {time.ctime()}:")
            
            target = data.get('target')
            tourist_id = data.get('tourist_id')
            
            if target == "DASHBOARD":
                print(f"  >> ACTION: Pushing to Police Dashboard via WebSocket...")
                print(f"  >> Tourist ID: {tourist_id}")
                print(f"  >> Reason: {data.get('reason')}")
                print(f"  >> Details: {data.get('details')}")

            elif target == "USER_APP":
                print(f"  >> ACTION: Sending Push Notification to User App (via FCM/APNS)...")
                print(f"  >> Tourist ID: {tourist_id}")
                print(f"  >> Message: '{data.get('message')}'")
                
            elif target == "NEARBY_TOURISTS":
                print(f"  >> ACTION: Querying for nearby users and sending group notification...")
                print(f"  >> Help needed for Tourist ID: {tourist_id}")
                print(f"  >> Last Known Location: {data.get('last_location')}")
            
            print("----------------------------------------")

if __name__ == "__main__":
    main()

