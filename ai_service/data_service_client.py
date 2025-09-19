import httpx
from config import DATA_SERVICE_URL

class DataServiceClient:
    def __init__(self):
        self.base_url = DATA_SERVICE_URL
        # Use a persistent client for connection pooling and better performance
        self.client = httpx.Client(base_url=self.base_url, timeout=5.0)

    def get_tourist_profile(self, tourist_id: int):
        """
        Makes a real API call to the Data Service to get a tourist's profile.
        """
        try:
            # This corresponds to the GET /tourists/{tourist_id} endpoint in our other service
            response = self.client.get(f"/tourists/{tourist_id}")
            response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
            return response.json()
        except httpx.RequestError as e:
            print(f"  [Data Service Client] ERROR: Could not connect to Data Service at {e.request.url}.")
            return None # Return None if the service is down
        except httpx.HTTPStatusError as e:
            print(f"  [Data Service Client] ERROR: Received status {e.response.status_code} for tourist {tourist_id}.")
            return None

    def update_tourist_score(self, tourist_id: int, score: float, notifications: list):
        """
        Makes a real API call to update a tourist's status.
        NOTE: This endpoint would need to be created in the Data Service.
        """
        try:
            payload = {"safety_score": score, "notifications": notifications}
            # This would be a new endpoint, e.g., PATCH /tourists/{tourist_id}/status
            response = self.client.patch(f"/tourists/{tourist_id}/status", json=payload)
            response.raise_for_status()
            print(f"  [Data Service Client] Successfully updated score for tourist {tourist_id}.")
            return True
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"  [Data Service Client] ERROR: Failed to update score for tourist {tourist_id}. Error: {e}")
            return False
