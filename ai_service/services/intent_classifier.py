from google import genai
import time

# Initialize Gemini API client
client = genai.Client(api_key="AIzaSyBC-qFFjs5gFAAq52lynq3xfG9uumlfkoI")

def service_classify_intent(user_query: str) -> dict:
    prompt = f"""
You are an intelligent travel safety assistant system that performs the following tasks:

1. Classify a user's query into one of these intent types:
    - Static — The answer can be retrieved from static knowledge stored in the system (e.g., "What documents are needed for Arunachal Pradesh?", "How to lodge an e-FIR?").
    - Dynamic — The query requires real-time data retrieval or execution of a function/API call (e.g., "Find nearest embassy", "Show route to airport", "Compute safety score").
    - Hybrid — The query requires both static knowledge and dynamic functionality (e.g., "I lost my passport, what should I do and where is the nearest embassy?").

2. If the intent is Dynamic or Hybrid, also identify the entity or functionality involved from this list:
    - locate_authorities         (e.g., nearest embassy, nearest hospital, nearest police station)
    - geofencing_safety_score    (e.g., calculate safety score, get geofencing alerts)
    - route_finder               (e.g., route to railway station, path to airport)
    - lodge_e_fir                (e.g., lodge an e-FIR, report a stolen item)
    - panic_alert                (e.g., activate panic alert)
    - get_weather                (e.g., current weather in area)

Return exactly two lines:
1. First line: One of "Static", "Dynamic", or "Hybrid".
2. Second line: The identified entity or "None" if Static.

Example Output:
Dynamic
locate_authorities

Now classify and extract the entity for this query:

Query: "{user_query}"
"""

    print(f"Calling Gemini API for intent classification and entity extraction of query: {user_query}")

    try:
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt
        )
        result = response.text.strip().splitlines()

        if len(result) != 2:
            print(f"Unexpected API response format: {result}")
            return {"intent": "Unknown", "entity": "None"}

        intent = result[0].strip().capitalize()
        entity = result[1].strip().lower()

        valid_entities = [
            "locate_authorities",
            "geofencing_safety_score",
            "route_finder",
            "lodge_e_fir",
            "panic_alert",
            "get_weather",
            "none"
        ]

        if intent not in ["Static", "Dynamic", "Hybrid"]:
            intent = "Unknown"
        if entity not in valid_entities:
            entity = "None"

        print(f"Intent classified as: {intent}, Entity detected: {entity}")
        return {"intent": intent, "entity": entity}

    except Exception as e:
        print(f"Error during intent classification: {e}")
        return {"intent": "Error", "entity": "None"}

    finally:
        time.sleep(1)  # Respect API rate limits