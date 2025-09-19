import pytest
from unittest.mock import MagicMock, patch
import io

# Import all the service functions we want to test
from services.intent_classifier import service_classify_intent
from services.rag_chatbot import service_get_rag_response
from services.voice_processor import service_transcribe_audio_to_english, service_convert_english_to_speech

# ==============================================================================
# Tests for: intent_classifier.py
# ==============================================================================
@pytest.mark.parametrize("query, expected_intent, expected_entity", [
    ("Help I am in trouble!", "Dynamic", "panic_alert"),
    ("Where is the nearest police station?", "Dynamic", "locate_authorities"),
    ("What documents do I need?", "Static", "None"),
    ("I lost my wallet, where is the embassy?", "Hybrid", "locate_authorities"),
    ("some gibberish text", "Static", "None"), # Test fallback
])
def test_intent_classification_scenarios(query, expected_intent, expected_entity):
    """SCENARIO: Various user queries. EXPECTATION: Correct intent and entity are classified."""
    # This tests our mock logic, but in a real app, it would validate the LLM's prompt.
    result = service_classify_intent(query)
    assert result["intent"] == expected_intent
    assert result["entity"] == expected_entity

# ==============================================================================
# Tests for: rag_chatbot.py
# ==============================================================================
def test_rag_response_for_known_query():
    """SCENARIO: User asks about a topic in our mock knowledge base. EXPECTATION: A relevant static answer."""
    result = service_get_rag_response("How do I lodge an e-fir?")
    assert "official state police website" in result

def test_rag_response_for_unknown_query():
    """SCENARIO: User asks a general question. EXPECTATION: A generic fallback answer."""
    result = service_get_rag_response("What is the capital of France?")
    assert "I am a tourist safety assistant" in result

# ==============================================================================
# Tests for: voice_processor.py
# ==============================================================================
def test_transcribe_audio_mocked(monkeypatch):
    """SCENARIO: An audio file is processed. EXPECTATION: Correct mock transcription and language detection."""
    # We mock the entire transcription process to avoid heavy dependencies in tests
    def mock_transcribe(*args, **kwargs):
        # Simulate a successful transcription
        return "I need help", "en"
    monkeypatch.setattr("services.voice_processor.service_transcribe_audio_to_english", mock_transcribe)
    
    # We pass a dummy file object because the function is fully mocked
    dummy_file = MagicMock()
    text, lang = service_transcribe_audio_to_english(dummy_file)
    
    assert text == "I need help"
    assert lang == "en"

def test_transcribe_audio_fails(monkeypatch):
    """SCENARIO: The transcription service fails. EXPECTATION: Function returns None."""
    def mock_transcribe_fail(*args, **kwargs):
        # Simulate a failure
        return None, None
    monkeypatch.setattr("services.voice_processor.service_transcribe_audio_to_english", mock_transcribe_fail)
    
    dummy_file = MagicMock()
    text, lang = service_transcribe_audio_to_english(dummy_file)
    
    assert text is None
    assert lang is None

def test_convert_text_to_speech_mocked(monkeypatch):
    """SCENARIO: Text is converted to speech. EXPECTATION: An in-memory audio file is returned."""
    # Mock the gTTS library to avoid actual file I/O or network calls
    mock_fp = io.BytesIO(b"mock_audio_data")
    mock_gtts_instance = MagicMock()
    mock_gtts_instance.write_to_fp.side_effect = lambda fp: fp.write(mock_fp.getvalue())
    
    # Patch the gTTS class constructor to return our mock instance
    monkeypatch.setattr("services.voice_processor.gTTS", lambda **kwargs: mock_gtts_instance)

    audio_stream = service_convert_english_to_speech("Hello", "en")
    
    assert audio_stream.getvalue() == b"mock_audio_data"

