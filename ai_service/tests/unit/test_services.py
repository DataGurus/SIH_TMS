import time
import json
from unittest.mock import MagicMock
import pytest
import io

# Import all service functions
from services.location_dropoff import service_check_location_dropoff
from services.inactivity import service_check_inactivity
from services.buffer_zone import service_check_buffer_zone
from services.SOS import service_handle_sos
from services.efir import service_compile_efir_data
from services.intent_classifier import service_classify_intent
from services.rag_chatbot import service_get_rag_response
from services.voice_processor import service_transcribe_audio_to_english, service_convert_english_to_speech

# ==============================================================================
# Tests for Core Safety Services
# ==============================================================================

def test_location_dropoff_in_orange_zone_escalates(mock_redis_client: MagicMock):
    """SCENARIO: Signal lost > 30 mins in ORANGE zone. EXPECTATION: ALERT_DASHBOARD."""
    last_log = {"timestamp": time.time() - 1801, "risk_score_result": {"zone": "ORANGE"}}
    mock_redis_client.lindex.return_value = json.dumps(last_log)
    result = service_check_location_dropoff(1, mock_redis_client)
    assert result["action"] == "ALERT_DASHBOARD"

def test_inactivity_in_yellow_zone_alerts_nearby(mock_redis_client: MagicMock):
    """SCENARIO: Inactive > 30 mins in YELLOW zone. EXPECTATION: ALERT_NEARBY_TOURISTS."""
    logs = [
        {"timestamp": time.time() - 1, "speed_kmh": 0.0, "risk_score_result": {"zone": "YELLOW"}},
        {"timestamp": time.time() - 1801, "speed_kmh": 0.0},
    ]
    mock_redis_client.lrange.side_effect = [[json.dumps(log) for log in logs]] * 2
    result = service_check_inactivity(1, mock_redis_client)
    assert result["action"] == "ALERT_NEARBY_TOURISTS"

def test_sos_happy_path(mock_redis_client: MagicMock, mock_data_service_client: MagicMock):
    """SCENARIO: Valid SOS press. EXPECTATION: Correct alert payload is generated."""
    latest_log = {"latitude": 10, "longitude": 20}
    mock_redis_client.lindex.return_value = json.dumps(latest_log)
    result = service_handle_sos(1, mock_redis_client, mock_data_service_client)
    assert result["alert_type"] == "SOS_BUTTON_PRESS"
    assert result["tourist_info"]["name"] == "John Doe"

def test_efir_compilation_happy_path(mock_redis_client: MagicMock, mock_data_service_client: MagicMock):
    """SCENARIO: Valid E-FIR request. EXPECTATION: Data package is compiled correctly."""
    logs = [{"latitude": 10}, {"latitude": 11}]
    mock_redis_client.lrange.return_value = [json.dumps(log) for log in logs]
    incident = {"type": "THEFT"}
    result = service_compile_efir_data(1, incident, mock_redis_client, mock_data_service_client)
    assert result["incident_details"]["type"] == "THEFT"
    assert result["tourist_profile"]["name"] == "John Doe"
    assert len(result["location_trail"]) == 2

# ==============================================================================
# Tests for Chatbot and Voice Services
# ==============================================================================

@pytest.mark.parametrize("query, expected_intent, expected_entity", [
    ("Help I am in trouble!", "Dynamic", "panic_alert"),
    # CORRECTED: The test now expects the correct, lowercase 'none'
    ("What documents do I need?", "Static", "none"),
])
def test_intent_classification_scenarios(query, expected_intent, expected_entity):
    result = service_classify_intent(query)
    assert result["intent"] == expected_intent
    assert result["entity"] == expected_entity

def test_rag_response_for_known_query(monkeypatch):
    """
    SCENARIO: User asks a topic in the knowledge base.
    EXPECTATION: A relevant static answer is returned, without a real API call.
    """
    # CORRECTED: Mock the Gemini API call to isolate the test from the network
    mock_response = MagicMock()
    mock_response.text = "This is a restructured answer about the official state police website."
    
    # We patch the 'generate_content' method of the client object inside the rag_chatbot module
    monkeypatch.setattr("services.rag_chatbot.client.models.generate_content", lambda *args, **kwargs: mock_response)
    
    result = service_get_rag_response("How do I lodge an e-fir?")
    assert "official state police website" in result

def test_transcribe_audio_fails(monkeypatch):
    def mock_transcribe_fail(*args, **kwargs): return None, None
    monkeypatch.setattr("services.voice_processor.service_transcribe_audio_to_english", mock_transcribe_fail)
    text, lang = service_transcribe_audio_to_english(MagicMock())
    assert text is None

def test_convert_text_to_speech_mocked(monkeypatch):
    mock_fp = io.BytesIO(b"mock_audio_data")
    mock_gtts_instance = MagicMock()
    mock_gtts_instance.write_to_fp.side_effect = lambda fp: fp.write(mock_fp.getvalue())
    monkeypatch.setattr("services.voice_processor.gTTS", lambda **kwargs: mock_gtts_instance)
    audio_stream = service_convert_english_to_speech("Hello", "en")
    assert audio_stream.getvalue() == b"mock_audio_data"

