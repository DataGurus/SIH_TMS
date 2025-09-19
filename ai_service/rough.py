from fastapi import FastAPI, UploadFile, File, Form, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Smart Tourist Safety Monitoring & Incident Response System")

@app.get("/")
async def root():
    return {"message": "Welcome to the Smart Tourist Safety Monitoring & Incident Response System API"}

# 1. DigiLocker (VigiLocker) based verification
@app.post("/vigilocker/verify")
async def vigilocker_verify(document: UploadFile = File(...)):
    print("VigiLocker document received:", document.filename)
    return {"status": "Document received for verification"}

# 2. Snapshot and cosine similarity verification
@app.post("/face/verify")
async def face_verify(snapshot: UploadFile = File(...), reference: UploadFile = File(...)):
    print("Snapshot and reference images received for cosine similarity check")
    return {"status": "Face verification initiated"}

# 3. Chatbot and voicebot
class ChatRequest(BaseModel):
    message: str

@app.post("/chatbot")
async def chatbot(req: ChatRequest):
    print("Chatbot received message:", req.message)
    return {"reply": "This is a dummy chatbot reply."}

@app.post("/voicebot")
async def voicebot(req: ChatRequest):
    print("Voicebot received message:", req.message)
    return {"audio_url": "https://dummy-audio-url.com/audio.mp3"}

# 4. Safety score
@app.get("/safety_score")
async def get_safety_score(user_id: Optional[str] = None):
    print("Safety score requested for user:", user_id)
    return {"user_id": user_id, "safety_score": 85}

# 5. News, alerts, weather-based alerts, notifications
@app.get("/dashboard/notifications")
async def get_notifications():
    print("Dashboard notifications requested")
    return {"notifications": ["Dummy news", "Dummy alert", "Dummy weather alert"]}

# 6. Buffer zone entry notification
@app.post("/geofence/bufferzone")
async def bufferzone_entry(user_id: str = Body(...), zone_id: str = Body(...)):
    print(f"User {user_id} entered buffer zone {zone_id}")
    return {"status": "Buffer zone entry notification triggered"}

# 7. Inactivity detection
@app.post("/user/inactivity")
async def inactivity_detected(user_id: str = Body(...)):
    print(f"Inactivity detected for user {user_id}")
    return {"status": "Inactivity notification triggered"}

# 8. Sudden location dropoff
@app.post("/user/location_dropoff")
async def location_dropoff(user_id: str = Body(...)):
    print(f"Location dropoff detected for user {user_id}")
    return {"status": "Location dropoff notification triggered"}

# 9. SOS/Panic Button
@app.post("/user/sos")
async def sos_trigger(user_id: str = Body(...)):
    print(f"SOS triggered by user {user_id}")
    return {"status": "SOS notification sent"}

# 10. FIR filing (online/offline)
class FIRRequest(BaseModel):
    user_id: str
    description: str
    online: bool

@app.post("/fir/file")
async def file_fir(fir: FIRRequest):
    print(f"FIR filing requested by user {fir.user_id}, online: {fir.online}")
    if fir.online:
        return {"status": "FIR filed online"}
    else:
        return {"status": "FIR notification sent to police dashboard (offline)"}