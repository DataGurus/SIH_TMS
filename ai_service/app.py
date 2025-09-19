import time
import json
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

# FastAPI Imports (Modern)
# Added UploadFile and File for the voice bot endpoint
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from pydantic import BaseModel, Field
from starlette.responses import StreamingResponse

# Redis Imports (Modern)
import redis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from notification_client import NotificationClient
from data_service_client import DataServiceClient

# ==============================================================================
# 1. SERVICE IMPORTS
# ==============================================================================
# These functions are now self-sufficient and will fetch data from Redis as needed.
from services.buffer_zone import service_check_buffer_zone
from services.location_dropoff import service_check_location_dropoff
from services.inactivity import service_check_inactivity
from services.risk_score import service_calculate_risk_score
from services.SOS import service_handle_sos
from services.efir import service_compile_efir_data
from services.rag_chatbot import service_get_rag_response
from services.intent_classifier import service_classify_intent
from services.voice_processor import service_transcribe_audio_to_english, service_convert_english_to_speech

# ==============================================================================
# 2. APPLICATION SETUP & DATABASE CONNECTIONS
# ==============================================================================

app = FastAPI(
    title="Smart Tourist AI & Real-time Service (with Chatbot)",
    description="Implements a high-performance workflow with new chatbot endpoints.",
    version="8.0.0"
)

# --- Real Redis Connection ---
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    redis_client.ping()
    print("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"FATAL: Could not connect to Redis. Error: {e}")
    exit()
notification_client = NotificationClient(redis_client)
data_service_client = DataServiceClient() 

# --- Mock Interaction with the Data Service ---
mock_data_service_api = {
    "get_tourist_profile": lambda tourist_id: {
        1: {"id": 1, "name": "John Doe", "status": "Active", "emergency_contacts": [{"name": "Jane Doe", "phone": "555-1234"}]},
        2: {"id": 2, "name": "Alice Smith", "status": "Active", "emergency_contacts": [{"name": "Bob Smith", "phone": "555-5678"}]},
    }.get(tourist_id),
    "update_tourist_score": lambda tourist_id, score, notifications: print(f"  [Data Service] MOCK API CALL: Updating tourist {tourist_id} score to {score} in PostgreSQL.")
}

# --- Thread Pool for Concurrent Checks ---
executor = ThreadPoolExecutor(max_workers=4)


# ==============================================================================
# 3. CORE LOGIC ORCHESTRATOR
# ==============================================================================

def run_all_safety_checks(tourist_id: int) -> dict:
    """
    The orchestrator, which triggers self-sufficient checks.
    """
    print(f"\n--- Analysis Started for Tourist ID: {tourist_id} ---")
    notifications = []
    
    # Get the most recent log, which now includes the risk score
    latest_log_json = redis_client.lindex(f"tourist:{tourist_id}:logs", 0)
    if not latest_log_json:
        return {"final_safety_score": 0.0, "notifications": ["No recent location data found."]}
    latest_log = json.loads(latest_log_json)
    
    # State-aware red zone check
    is_currently_in_red_zone = latest_log["risk_score_result"].get("zone") == "RED"
    was_in_red_zone_flag = f"tourist:{tourist_id}:red_zone_alert"
    was_in_red_zone = redis_client.exists(was_in_red_zone_flag)

    if is_currently_in_red_zone and not was_in_red_zone:
        redis_client.set(was_in_red_zone_flag, "true", ex=3600)
        return {"final_safety_score": 10.0, "notifications": ["CRITICAL: You have entered a restricted area. Authorities have been notified."]}

    if not is_currently_in_red_zone and was_in_red_zone:
        redis_client.delete(was_in_red_zone_flag)
        notifications.append("You have left the restricted area. Resuming normal monitoring.")

    if is_currently_in_red_zone:
        return {"final_safety_score": 10.0, "notifications": ["You are still in a restricted area."]}
        
    # --- CONCURRENT STANDARD CHECKS ---
    future_buffer = executor.submit(service_check_buffer_zone, tourist_id, redis_client)
    future_dropoff = executor.submit(service_check_location_dropoff, tourist_id, redis_client) 
    future_inactivity = executor.submit(service_check_inactivity, tourist_id, redis_client)

    results = {
        "buffer": future_buffer.result(),
        "dropoff": future_dropoff.result(),
        "inactivity": future_inactivity.result()
    }
    
    # --- SYNTHESIZE RESULTS ---
    if results["buffer"].get("action") == "NOTIFY_USER_APP":
        notifications.append(f"Warning: You are approaching a high-risk area ({results['buffer'].get('reason')}).")
    
    base_risk_score = latest_log["risk_score_result"].get("score", 0)
    final_safety_score = base_risk_score
    if results["dropoff"].get("status") == "SIGNAL_LOST_WAITING":
        final_safety_score += 2.0 
    if results["inactivity"].get("status") == "INACTIVE_WAITING":
        final_safety_score += 1.5
    
    final_safety_score = min(final_safety_score, 10.0)

    mock_data_service_api["update_tourist_score"](tourist_id, round(final_safety_score, 2), notifications)
    
    print(f"--- Analysis Finished for Tourist ID: {tourist_id} ---\n")
    return {"final_safety_score": round(final_safety_score, 2), "notifications": list(set(notifications))}


# ==============================================================================
# 4. CHATBOT ORCHESTRATOR
# ==============================================================================

def handle_query_orchestration(tourist_id: int, user_query: str) -> (str, str):
    """
    Central orchestrator for handling all text-based queries.
    1. Classifies intent.
    2. Selects the correct tool (RAG, dynamic action, or both).
    3. Synthesizes a final response.
    Returns (response_text, intent)
    """
    # Step 1: Classify intent ONCE
    classification = service_classify_intent(user_query)
    intent = classification["intent"]
    entity = classification["entity"]
    
    response_text = ""
    
    # Step 2: Tool Selection
    if intent in ["Static", "Hybrid"]:
        response_text += service_get_rag_response(user_query)
        
    if intent in ["Dynamic", "Hybrid"]:
        if entity == "panic_alert":
            # For dynamic actions, we can call our existing services
            sos_result = service_handle_sos(tourist_id, redis_client, data_service_client)
            notification_client.send_dashboard_alert(tourist_id, "PANIC_ALERT_FROM_CHAT", sos_result)
            dynamic_response = "I have triggered a panic alert for you. Help is on the way."
        else:
            dynamic_response = "I understand you need a real-time action, but that specific function is not fully implemented yet."
        
        response_text = f"{response_text} {dynamic_response}".strip()

    if not response_text:
        response_text = "I'm sorry, I couldn't process that request. Please try rephrasing."
        
    return response_text, intent


# ==============================================================================
# 5. API MODELS (Pydantic V2 Syntax)
# ==============================================================================

class RealTimeLog(BaseModel):
    tourist_id: int = Field(..., example=1)
    latitude: float = Field(..., example=18.5204)
    longitude: float = Field(..., example=73.8567)
    speed_kmh: float = Field(..., example=5.2)
    battery_level: float = Field(..., example=0.85)
    timestamp: float = Field(default_factory=time.time)

class LogResponse(BaseModel):
    status: str = "processed"
    current_safety_score: float
    notifications: List[str]

class SosRequest(BaseModel):
    tourist_id: int = Field(..., example=1)

class EfirRequest(BaseModel):
    tourist_id: int = Field(..., example=1)
    incident_details: Dict = Field(..., example={"type": "THEFT", "description": "My wallet was stolen."})

# --- NEW Models for Chatbot ---
class ChatRequest(BaseModel):
    tourist_id: int = Field(..., example=1)
    text: str = Field(..., example="Where is the nearest hospital?")

class ChatResponse(BaseModel):
    response_text: str
    intent: str = "informational" # Default intent

# ==============================================================================
# 6. API ENDPOINTS
# ==============================================================================

@app.post("/logs/realtime", response_model=LogResponse)
async def capture_realtime_log(log: RealTimeLog):
    """
    High-frequency endpoint that enriches the log with a risk score before
    running synchronous, concurrent analysis.
    """
    risk_score_result = service_calculate_risk_score(log.latitude, log.longitude)
    enriched_log = log.model_dump()
    enriched_log["risk_score_result"] = risk_score_result
    
    log_key = f"tourist:{log.tourist_id}:logs"
    pipe = redis_client.pipeline()
    pipe.lpush(log_key, json.dumps(enriched_log))
    pipe.ltrim(log_key, 0, 1999)
    pipe.expire(log_key, 1800)
    pipe.execute()

    analysis_result = run_all_safety_checks(log.tourist_id)

    return LogResponse(
        current_safety_score=analysis_result["final_safety_score"],
        notifications=analysis_result["notifications"]
    )

@app.post("/sos")
async def trigger_sos(request: SosRequest):
    alert_payload = service_handle_sos(request.tourist_id, redis_client, mock_data_service_api)
    if "error" in alert_payload:
        raise HTTPException(status_code=404, detail=alert_payload["error"])
    return alert_payload

@app.post("/efir/compile")
async def compile_efir_package(request: EfirRequest):
    data_package = service_compile_efir_data(request.tourist_id, request.incident_details, redis_client, mock_data_service_api)
    if not data_package.get("tourist_profile"):
        raise HTTPException(status_code=404, detail="Tourist profile not found.")
    return data_package

# --- NEW CHATBOT ENDPOINTS ---

@app.post("/chatbot", response_model=ChatResponse)
async def handle_text_chat(request: ChatRequest):
    """ Handles a text-based query from a user. """
    response_text, intent = handle_query_orchestration(request.tourist_id, request.text)
    return ChatResponse(response_text=response_text, intent=intent)

@app.post("/voicebot")
async def handle_voice_chat(tourist_id: int = Form(...), audio_file: UploadFile = File(...)):
    """ Handles a voice-based query. Returns a streaming audio response. """
    # Voice Pipeline - Step 1: Transcribe and Translate
    english_text, source_lang = service_transcribe_audio_to_english(audio_file)
    if not english_text:
        raise HTTPException(status_code=400, detail="Could not understand audio.")

    # Voice Pipeline - Step 2: Orchestrate response
    response_text_english, _ = handle_query_orchestration(tourist_id, english_text)

    # Voice Pipeline - Step 3: Translate back and convert to speech
    audio_stream = service_convert_english_to_speech(response_text_english, source_lang)
    
    # Return the in-memory audio file as a streaming response
    return StreamingResponse(audio_stream, media_type="audio/mpeg")