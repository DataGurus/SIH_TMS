from flask import Flask, request, jsonify, render_template
import requests
import cv2
import numpy as np
import mediapipe as mp
import os
import json
import base64

# ✅ Import the right functions
from face2embed import extract_key_landmarks, calculate_similarity  

app = Flask(__name__)

# URL of your fake DigiLocker (VigiLocker)
VIGILOCKER_URL = "http://127.0.0.1:5001/verify"

# Initialize Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Load stored facial landmarks
with open("user_landmarks.json", "r") as f:
    user_landmarks = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/verify_user", methods=["POST"])
def verify_user():
    data = request.json
    print("Received data:", {key: value for key, value in data.items() if key != "photo"})  # Exclude Base64 photo

    name = data.get("name")
    doc_number = data.get("document_number")
    photo_data = data.get("photo")

    # Decode the photo from base64
    try:
        photo_bytes = base64.b64decode(photo_data.split(",")[1])
        photo_array = np.frombuffer(photo_bytes, dtype=np.uint8)
        photo = cv2.imdecode(photo_array, cv2.IMREAD_COLOR)
        print("Decoded photo shape:", photo.shape if photo is not None else "None")
    except Exception as e:
        print("Error decoding photo:", str(e))
        return jsonify({"status": "failed", "reason": "Invalid photo input"}), 400

    # Validate the input image
    if photo is None or photo.size == 0:
        print("Invalid photo input")
        return jsonify({"status": "failed", "reason": "Invalid photo input"}), 400

    # Process the image with Mediapipe
    print("Processing image with Mediapipe...")
    try:
        rgb_img = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_img)
        print("Mediapipe processing completed")
    except Exception as e:
        print("Error during Mediapipe processing:", str(e))
        return jsonify({"status": "failed", "reason": "Error during face processing"}), 500

    if results.multi_face_landmarks:
        print("Face landmarks detected")
        landmarks = results.multi_face_landmarks[0]
        embeddings = extract_key_landmarks(landmarks.landmark)  # ✅ correct call
        print("Extracted embeddings:", embeddings)
    else:
        print("No face landmarks detected")
        return jsonify({"status": "failed", "reason": "No face detected"}), 400

    # Optional local similarity check
    stored_landmarks = user_landmarks.get("USR001")  # replace dynamically
    if stored_landmarks:
        try:
            similarity_score = calculate_similarity(embeddings, stored_landmarks)
            print("Stored landmarks:", stored_landmarks)
            print("Similarity score:", similarity_score)
        except Exception as e:
            print("Error calculating similarity:", str(e))

    # Send data to VigiLocker
    try:
        payload = {
            "name": name,
            "document_number": doc_number,
            "embeddings": embeddings
        }
        print("Sending payload to VigiLocker:", payload)
        response = requests.post(VIGILOCKER_URL, json=payload)
        print("VigiLocker response status:", response.status_code)
        print("VigiLocker response data:", response.json())
    except Exception as e:
        print("Error communicating with VigiLocker:", str(e))
        return jsonify({"status": "failed", "reason": "Error communicating with VigiLocker"}), 500

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"status": "failed", "reason": "Verification failed"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
