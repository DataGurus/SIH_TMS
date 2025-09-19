import json
from config import NOTIFICATION_CHANNEL

class NotificationClient:
    """
    A client responsible for publishing structured alert messages to a Redis channel.
    This decouples the decision-making logic from the notification-sending mechanism.
    """
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def _publish(self, message: dict):
        """Helper to publish a message to the Redis channel."""
        print(f"  [Notification Client] Publishing message: {message}")
        self.redis_client.publish(NOTIFICATION_CHANNEL, json.dumps(message))

    def send_dashboard_alert(self, tourist_id: int, reason: str, details: dict = None):
        """Sends a structured alert intended for the police dashboard."""
        payload = {
            "target": "DASHBOARD",
            "tourist_id": tourist_id,
            "reason": reason,
            "details": details or {}
        }
        self._publish(payload)

    def send_user_notification(self, tourist_id: int, message: str, alert_type: str):
        """Sends a notification intended for the specific tourist's mobile app."""
        payload = {
            "target": "USER_APP",
            "tourist_id": tourist_id,
            "type": alert_type,
            "message": message
        }
        self._publish(payload)

    def send_nearby_tourist_alert(self, tourist_id: int, last_location: dict):
        """Sends a broadcast-style alert for tourists in a specific geographic area."""
        payload = {
            "target": "NEARBY_TOURISTS",
            "tourist_id": tourist_id,
            "last_location": last_location
        }
        self._publish(payload)

