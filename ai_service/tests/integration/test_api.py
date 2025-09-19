import json
from fastapi.testclient import TestClient

# ==============================================================================
# Tests for: Core Safety Endpoints
# ==============================================================================
def test_realtime_log_endpoint_success(test_client: TestClient, monkeypatch):
    """
    SCENARIO: The mobile app sends a standard, non-critical location log.
    EXPECTATION: The API should return a 200 OK status and a valid LogResponse.
    """
    def mock_run_checks(tourist_id):
        return {"final_safety_score": 3.5, "notifications": ["All systems normal."]}
    monkeypatch.setattr("app.run_all_safety_checks", mock_run_checks)

    log_payload = {"tourist_id": 1, "latitude": 18.5, "longitude": 73.8, "speed_kmh": 5.0, "battery_level": 0.9}
    response = test_client.post("/logs/realtime", json=log_payload)
    
    assert response.status_code == 200
    assert response.json()["current_safety_score"] == 3.5

# ==============================================================================
# Tests for: Chatbot Endpoints
# ==============================================================================
def test_chatbot_endpoint_static_intent(test_client: TestClient, monkeypatch):
    """
    SCENARIO: A user sends a text query with a static intent.
    EXPECTATION: The orchestrator is called, and a valid chat response is returned.
    """
    def mock_orchestrator(tourist_id, user_query):
        return "This is a static answer.", "Static"
    monkeypatch.setattr("app.handle_query_orchestration", mock_orchestrator)
    
    chat_payload = {"tourist_id": 1, "text": "What are the rules?"}
    response = test_client.post("/chatbot", json=chat_payload)
    assert response.status_code == 200
    assert response.json()["intent"] == "Static"

def test_voicebot_endpoint(test_client: TestClient, monkeypatch):
    """
    SCENARIO: A user uploads an audio file.
    EXPECTATION: The full voice pipeline is executed and an audio stream is returned.
    """
    def mock_transcribe(*args, **kwargs): return "I need help", "hi"
    # CORRECTED PATH: Point to the function's true location inside the 'services' package
    monkeypatch.setattr("services.voice_processor.service_transcribe_audio_to_english", mock_transcribe)
    
    def mock_orchestrator(*args, **kwargs): return "Help is on the way.", "Dynamic"
    monkeypatch.setattr("app.handle_query_orchestration", mock_orchestrator)
    
    def mock_tts(*args, **kwargs):
        import io
        return io.BytesIO(b"mock_hindi_audio")
    # CORRECTED PATH: Point to the function's true location inside the 'services' package
    monkeypatch.setattr("services.voice_processor.service_convert_english_to_speech", mock_tts)

    files = {'audio_file': ('test.wav', b'dummy_audio_content', 'audio/wav')}
    data = {'tourist_id': 1}
    response = test_client.post("/voicebot", data=data, files=files)

    assert response.status_code == 200
    assert response.headers['content-type'] == 'audio/mpeg'
    assert response.content == b'mock_hindi_audio'

