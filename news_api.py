"""
Tourist Monitoring - Notification & Safety Score Service
Single-file FastAPI app that exposes endpoints for:
 - Admin: create alerts (crime, traffic, calamity, event)
 - User: update location (triggers geofence checks, safety score recompute, notifications)
 - Weather check: fetch weather & create predictive alerts
 - Query: get nearby alerts, get safety score

Notes:
 - Fill in OPENWEATHER_API_KEY, TWILIO credentials, FCM / push provider credentials to enable push/SMS.
 - This is a self-contained starter that you can integrate into your existing dashboard and mobile app.
 - For production, split into modules, secure endpoints, add auth, rate-limiting, retries, logging, and tests.

Run:
    pip install fastapi uvicorn sqlalchemy pydantic requests python-dotenv
    uvicorn notification_service_main:app --reload --port 8000

Example curl (create alert):
  curl -X POST "http://localhost:8000/admin/alerts" -H "Content-Type: application/json" -d \
    '{"title":"Pickpocketing incidents","type":"crime","lat":12.9716,"lon":77.5946,"radius_m":2000,"severity":"medium","expires_at":null,"message":"Pickpocketing reported near MG Road"}'

"""
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from typing import Optional
from datetime import datetime, timedelta
import math
import requests
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

WEATHERAPI_KEY = os.getenv('Weather')
print(WEATHERAPI_KEY)
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM')
DATABASE_URL = "sqlite:///./alerts.db"

class NewsIngestRequest(BaseModel):
    title: str
    text: str
    lat: Optional[float] = None
    lon: Optional[float] = None

# Database (SQLite for demo)
def ingest_news(request: NewsIngestRequest):
    title = request.title
    text = request.text
    lat = request.lat
    lon = request.lon
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # crime, traffic, calamity, event, weather
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    radius_m = Column(Integer, default=1000)
    severity = Column(String, default='low')
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)

# Pydantic models
class AlertCreate(BaseModel):
    title: str
    type: str
    lat: float
    lon: float
    radius_m: int = 1000
    severity: str = 'low'
    message: Optional[str] = None
    expires_at: Optional[datetime] = None

class AlertOut(BaseModel):
    id: int
    title: str
    type: str
    lat: float
    lon: float
    radius_m: int
    severity: str
    message: Optional[str]
    created_at: datetime
    expires_at: Optional[datetime]


class LocationUpdate(BaseModel):
    lat: float
    lon: float
    user_id: str
    phone: Optional[str] = None  # for SMS if required

# Request model for weather check
class WeatherCheckRequest(BaseModel):
    lat: float
    lon: float


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Tourist Notification Service")

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utilities
def haversine_distance(lat1, lon1, lat2, lon2):
    # returns distance in meters
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Safety score logic
def compute_zone_safety_score(base_score: int, alerts_nearby: List[Alert]) -> int:
    """Combine base score with nearby alerts to compute new safety score (0-100).
    Higher severity reduces score more.
    """
    score = base_score
    for a in alerts_nearby:
        if a.severity == 'low':
            score -= 5
        elif a.severity == 'medium':
            score -= 20
        elif a.severity == 'high':
            score -= 50
    score = max(0, min(100, score))
    return score

# Notification stubs
def send_push_notification(user_id: str, title: str, message: str, data: dict = None):
    # Implement with FCM / OneSignal / your push provider. This is a stub.
    print(f"[PUSH] to {user_id}: {title} - {message} | data={data}")

def send_sms(phone: str, message: str):
    if not (TWILIO_SID and TWILIO_TOKEN and TWILIO_FROM):
        print(f"[SMS stub] Would send to {phone}: {message}")
        return
    from requests.auth import HTTPBasicAuth
    payload = {
        'From': TWILIO_FROM,
        'To': phone,
        'Body': message
    }
    # Note: Twilio REST API would usually be used via twilio-python package; using requests simplified.
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    r = requests.post(url, data=payload, auth=HTTPBasicAuth(TWILIO_SID, TWILIO_TOKEN))
    print('[SMS] status:', r.status_code, r.text)

# Weather integration (OpenWeatherMap example)
# def fetch_weather(lat: float, lon: float):
#     if OPENWEATHER_API_KEY == 'YOUR_OPENWEATHER_KEY' or not OPENWEATHER_API_KEY:
#         return None
#     url = 'https://api.openweathermap.org/data/2.5/onecall'
#     params = {
#         'lat': lat,
#         'lon': lon,
#         'exclude': 'minutely,alerts',
#         'appid': OPENWEATHER_API_KEY,
#         'units': 'metric'
#     }
#     r = requests.get(url, params=params, timeout=10)
#     if r.status_code != 200:
#         return None
#     return r.json()

# def analyze_weather_and_create_alert(lat: float, lon: float, session, background_tasks: BackgroundTasks = None):
#     data = fetch_weather(lat, lon)
#     if not data:
#         return None
#     # Simple heuristic: check hourly precipitation or extreme temp
#     # If heavy rain or storm in next 6 hours, create a high severity alert
#     for hour in data.get('hourly', [])[:6]:
#         pop = hour.get('pop', 0)  # probability of precipitation 0-1
#         rain = hour.get('rain', {}).get('1h', 0) if isinstance(hour.get('rain', {}), dict) else 0
#         wind = hour.get('wind_speed', 0)
#         temp = hour.get('temp')
#         if pop >= 0.6 or rain >= 10 or wind >= 15 or (temp is not None and temp >= 45):
#             # create alert
#             a = Alert(
#                 title='Weather Warning',
#                 type='weather',
#                 lat=lat,
#                 lon=lon,
#                 radius_m=5000,
#                 severity='high',
#                 message=f'Weather warning: pop={pop}, rain={rain}, wind={wind}, temp={temp}',
#                 created_at=datetime.utcnow(),
#                 expires_at=datetime.utcnow() + timedelta(hours=12)
#             )
#             session.add(a)
#             session.commit()
#             session.refresh(a)
#             # Optionally notify users in area (left to caller)
#             print('[WEATHER] created alert', a.id)
#             return a
#     return None
def fetch_weather(lat: float, lon: float):
    if not WEATHERAPI_KEY:
        return None
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": f"{lat},{lon}",
        "aqi": "no"
    }
    r = requests.get(url, params=params, timeout=10)
    if r.status_code != 200:
        print("WeatherAPI error:", r.text)
        return None
    return r.json()

def analyze_weather_and_create_alert(lat: float, lon: float, session, background_tasks: BackgroundTasks = None):
    data = fetch_weather(lat, lon)
    if not data:
        return None
    current = data.get("current", {})
    temp = current.get("temp_c")
    wind = current.get("wind_kph", 0)
    precip = current.get("precip_mm", 0)
    condition = current.get("condition", {}).get("text", "")

    # Simple heuristic: flag extreme conditions
    if precip >= 20 or wind >= 60 or (temp is not None and (temp >= 45 or temp <= 0)):
        a = Alert(
            title="Weather Warning",
            type="weather",
            lat=lat,
            lon=lon,
            radius_m=5000,
            severity="high",
            message=f"Weather warning: {condition}, temp={temp}°C, rain={precip}mm, wind={wind} kph",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=12)
        )
        session.add(a)
        session.commit()
        session.refresh(a)
        print("[WEATHER] created alert", a.id)
        return a
    return None
# Simple NLP stub to classify news text into safety-impacting or not
def classify_news_text_for_safety(text: str) -> bool:
    # Replace with real NLP model in production. For demo, keyword-based.
    keywords = ['protest', 'riot', 'attack', 'robbery', 'flood', 'landslide', 'earthquake', 'fire', 'shooting']
    txt = text.lower()
    return any(k in txt for k in keywords)

# DB helper: get active alerts near a location
def get_alerts_nearby(session, lat: float, lon: float, radius_m: int = 2000) -> List[Alert]:
    now = datetime.utcnow()
    rows = session.query(Alert).filter((Alert.expires_at == None) | (Alert.expires_at > now)).all()
    nearby = []
    for r in rows:
        d = haversine_distance(lat, lon, r.lat, r.lon)
        if d <= max(radius_m, r.radius_m):
            nearby.append(r)
    return nearby

# API Endpoints
@app.post('/admin/alerts', response_model=AlertOut)
def create_alert(alert: AlertCreate):
    session = SessionLocal()
    a = Alert(
        title=alert.title,
        type=alert.type,
        lat=alert.lat,
        lon=alert.lon,
        radius_m=alert.radius_m,
        severity=alert.severity,
        message=alert.message,
        created_at=datetime.utcnow(),
        expires_at=alert.expires_at
    )
    session.add(a)
    session.commit()
    session.refresh(a)
    session.close()
    return a

@app.get('/alerts/nearby', response_model=List[AlertOut])
def alerts_nearby(lat: float, lon: float, radius_m: int = 2000):
    session = SessionLocal()
    alerts = get_alerts_nearby(session, lat, lon, radius_m)
    out = [AlertOut(
        id=a.id, title=a.title, type=a.type, lat=a.lat, lon=a.lon,
        radius_m=a.radius_m, severity=a.severity, message=a.message,
        created_at=a.created_at, expires_at=a.expires_at
    ) for a in alerts]
    session.close()
    return out

@app.post('/users/{user_id}/location')
def user_location_update(user_id: str, loc: LocationUpdate, background_tasks: BackgroundTasks):
    """Called by the mobile app whenever the user's location updates.
    - Check nearby alerts
    - Compute safety score
    - Push notification if new/critical alerts
    - Send SMS if severity high and phone provided
    """
    session = SessionLocal()
    alerts = get_alerts_nearby(session, loc.lat, loc.lon, radius_m=2000)
    score = compute_zone_safety_score(100, alerts)

    # Basic: send push for any alert with severity medium+
    for a in alerts:
        if a.severity in ('medium', 'high'):
            background_tasks.add_task(send_push_notification, user_id, a.title, a.message or '', {
                'alert_id': a.id, 'severity': a.severity
            })
            if a.severity == 'high' and loc.phone:
                background_tasks.add_task(send_sms, loc.phone, f'EMERGENCY: {a.title} - {a.message}')

    session.close()
    return {
        'user_id': user_id,
        'safety_score': score,
        'nearby_alerts': [
            {'id': a.id, 'title': a.title, 'type': a.type, 'severity': a.severity} for a in alerts
        ]
    }

@app.get('/users/{user_id}/safety_score')
def get_user_safety_score(user_id: str, lat: float, lon: float):
    session = SessionLocal()
    alerts = get_alerts_nearby(session, lat, lon, radius_m=2000)
    score = compute_zone_safety_score(100, alerts)
    session.close()
    return {'user_id': user_id, 'safety_score': score}

# @app.post('/weather/check')
# def weather_check(request: WeatherCheckRequest, background_tasks: BackgroundTasks):
#     print("/weather/check called with:", request)
#     print("Loaded OWM_API:", OPENWEATHER_API_KEY)
#     session = SessionLocal()
#     lat = request.lat
#     lon = request.lon
#     print(f"Received coordinates: lat={lat}, lon={lon}")
#     # Debug: print the payload as dict
#     print("Request dict:", request.dict())
#     # Fetch weather and print API response status/content
#     url = 'https://api.openweathermap.org/data/2.5/onecall'
#     params = {
#         'lat': lat,
#         'lon': lon,
#         'exclude': 'minutely,alerts',
#         'appid': OPENWEATHER_API_KEY,
#         'units': 'metric'
#     }
#     print("Weather API request URL:", url)
#     print("Weather API params:", params)
#     r = requests.get(url, params=params, timeout=10)
#     print("Weather API status:", r.status_code)
#     print("Weather API response:", r.text)
#     if r.status_code != 200:
#         session.close()
#         return {'error': 'Weather data not available. Check API key or coordinates.'}
#     weather_data = r.json()
#     a = analyze_weather_and_create_alert(lat, lon, session, background_tasks)
#     session.close()
#     # Extract current weather features
#     current = weather_data.get('current', {})
#     temp = current.get('temp')
#     rainfall = 0
#     if 'rain' in current:
#         rain_val = current['rain']
#         if isinstance(rain_val, dict):
#             rainfall = rain_val.get('1h', 0)
#         else:
#             rainfall = rain_val
#     wind_speed = current.get('wind_speed')
#     humidity = current.get('humidity')
#     weather_desc = current.get('weather', [{}])[0].get('description')
#     # Return all available features
#     result = {
#         'temperature': temp,
#         'rainfall_mm_last_hour': rainfall,
#         'wind_speed': wind_speed,
#         'humidity': humidity,
#         'weather_description': weather_desc,
#         'raw_weather': current
#     }
#     if a:
#         result['created_alert_id'] = a.id
#         result['alert_message'] = 'Weather-based alert created.'
#     print("/weather/check output:", result)
#     return result
@app.post("/weather/check")
def weather_check(request: WeatherCheckRequest, background_tasks: BackgroundTasks):
    session = SessionLocal()
    lat, lon = request.lat, request.lon
    weather_data = fetch_weather(lat, lon)
    a = analyze_weather_and_create_alert(lat, lon, session, background_tasks)
    session.close()

    if not weather_data:
        return {"error": "Weather data not available. Check API key or coordinates."}

    current = weather_data.get("current", {})
    result = {
        "temperature": current.get("temp_c"),
        "rainfall_mm": current.get("precip_mm"),
        "wind_kph": current.get("wind_kph"),
        "humidity": current.get("humidity"),
        "condition": current.get("condition", {}).get("text"),
    }
    if a:
        result["created_alert_id"] = a.id
        result["alert_message"] = "Weather-based alert created."
    return result

@app.post('/news/ingest')
def ingest_news(request: NewsIngestRequest):
    """Ingest a piece of news/article text. If classified as safety-impacting, create an alert.
    Dashboard can call this with news items.
    """
    session = SessionLocal()
    title = request.title
    text = request.text
    lat = request.lat
    lon = request.lon
    is_safety = classify_news_text_for_safety(text)
    if is_safety:
        a = Alert(
            title=f'News: {title}',
            type='news',
            lat=lat if lat is not None else 0.0,
            lon=lon if lon is not None else 0.0,
            radius_m=5000,
            severity='medium',
            message=text[:1000],
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        session.add(a)
        session.commit()
        session.refresh(a)
        session.close()
        return {'created_alert_id': a.id}
    session.close()
    return {'message': 'Not classified as safety-impacting.'}

# Admin endpoint to force-adjust safety score for a polygon/area would be implemented by creating a special 'score adjustment' alert type

# Health check
@app.get('/health')
def health():
    return {'status': 'ok', 'time': datetime.utcnow().isoformat()}
