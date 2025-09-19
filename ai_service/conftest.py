import pytest
import redis
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

# Import the main FastAPI app object from the parent directory
from app import app

# --- Mocking the Redis Client ---
@pytest.fixture(scope="function")
def mock_redis_client():
    """ Provides a fresh mock Redis client for each test function. """
    mock_redis = MagicMock(spec=redis.Redis)
    mock_redis.lindex.return_value = None 
    mock_redis.exists.return_value = False
    mock_redis.hget.return_value = None
    mock_redis.lrange.return_value = []
    return mock_redis

# --- Mocking the Data Service API Client ---
@pytest.fixture
def mock_data_service_client():
    """
    Provides a mock of the data service API client. This simulates the
    responses from our other (Python 3.9) microservice.
    """
    mock_client = MagicMock()
    
    # Configure the side effect for the get_tourist_profile method
    def get_profile(tourist_id: int):
        if tourist_id == 1:
            return {"id": 1, "name": "John Doe", "emergency_contacts": [{"name": "Jane Doe"}]}
        return None # Simulate tourist not found
        
    mock_client.get_tourist_profile.side_effect = get_profile
    mock_client.update_tourist_score.return_value = True
    
    return mock_client

# --- Fixture for the FastAPI Test Client ---
@pytest.fixture(scope="module")
def test_client():
    """ Creates a FastAPI TestClient for integration tests. """
    client = TestClient(app)
    yield client

