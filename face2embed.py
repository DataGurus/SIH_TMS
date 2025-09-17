import cv2
import mediapipe as mp
import os
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Path to your photos
photo_dir = "/media/piyuwin/StorageHDD/SIH_TMS/photos"
photos = {
    "USR001": "PP.jpeg",
    "USR002": "Yashu.jpeg",
    "USR003": "SK.jpeg",
    "USR004": "Yo.jpeg",
    "USR005": "Jadoo.jpeg",
    "USR006": "Kaka.jpeg"
}

landmarks_data = {}

# ✅ New helper: works directly on Mediapipe landmarks
def extract_key_landmarks(landmarks):
    """Takes Mediapipe landmarks and returns only key regions."""
    return {
        "left_eye": [(landmarks[i].x, landmarks[i].y, landmarks[i].z) for i in [33, 133]],
        "right_eye": [(landmarks[i].x, landmarks[i].y, landmarks[i].z) for i in [362, 263]],
        "nose": [(landmarks[i].x, landmarks[i].y, landmarks[i].z) for i in [1, 2, 98]],
        "mouth": [(landmarks[i].x, landmarks[i].y, landmarks[i].z) for i in [61, 291]]
    }

# ✅ Refactored: works with image file paths
def get_key_landmarks_from_image(image_path):
    img = cv2.imread(image_path)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_img)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]
        return extract_key_landmarks(landmarks.landmark)
    else:
        return None

# Build JSON for known users
for user_id, filename in photos.items():
    path = os.path.join(photo_dir, filename)
    try:
        key_landmarks = get_key_landmarks_from_image(path)
        if key_landmarks:
            landmarks_data[user_id] = key_landmarks
            print(f"[OK] {user_id} key landmarks stored")
        else:
            print(f"[WARN] No face detected in {filename}")
            landmarks_data[user_id] = None
    except Exception as e:
        print(f"[ERROR] Failed to process {filename}: {e}")
        landmarks_data[user_id] = None

# Save JSON
with open("user_landmarks.json", "w") as f:
    json.dump(landmarks_data, f, indent=2)

print("✅ Saved key facial landmarks to user_landmarks.json")

# Function to calculate cosine similarity between two sets of landmarks
def calculate_similarity(landmarks1, landmarks2):
    similarities = []
    for region in ["left_eye", "right_eye", "nose", "mouth"]:
        if region in landmarks1 and region in landmarks2:
            sim = cosine_similarity(
                [np.array(landmarks1[region]).flatten()],
                [np.array(landmarks2[region]).flatten()]
            )[0][0]
            similarities.append(sim)

    return np.mean(similarities) if similarities else 0.0
