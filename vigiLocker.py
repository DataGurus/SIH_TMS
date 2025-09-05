from flask import Flask, request, jsonify
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Load facial landmarks from user_landmarks.json
with open("user_landmarks.json", "r") as f:
    user_landmarks = json.load(f)

# Helper function to normalize document numbers
def normalize_doc(doc: str) -> str:
    return doc.replace(" ", "").upper().strip()

# Dummy database with 7 entries
dummy_users = {
    "USR001": {
        "name": "Prasanna Patwardhan",
        "aadhaar": "123456789012",
        "pan": "ABCDE1234F",
        "passport": "N1234567",
        "photo": "/home/piyush/Desktop/SIH_TMS/photos/PP.jpeg",
        "landmarks": user_landmarks.get("USR001")
    },
    "USR002": {
        "name": "Yash Kulkarni",
        "aadhaar": "987654321098",
        "pan": "PQRSX5678Y",
        "passport": "M7654321",
        "photo": "/home/piyush/Desktop/SIH_TMS/photos/Yashu,peg",
        "landmarks": user_landmarks.get("USR002")
    },
    "USR003": {
        "name": "Sakshi Kuthwad",
        "aadhaar": "111122223333",
        "pan": "SAKSH1234M",
        "passport": "Z7654321",
        "photo": "/home/piyush/Desktop/SIH_TMS/photos/SK.jpeg",
        "landmarks": user_landmarks.get("USR003")
    },
    "USR004": {
        "name": "Yugandhar Chawale",
        "aadhaar": "444455556666",
        "pan": "YUGAN5678P",
        "passport": "Y1234567",
        "photo": "/home/piyush/Desktop/SIH_TMS/photos/Yo.jpeg",
        "landmarks": user_landmarks.get("USR004")
    },
    "USR005": {
        "name": "Rahul Dewani",
        "aadhaar": "777788889999",
        "pan": "RAHUL8765D",
        "passport": "X4567890",
        "photo": "/home/piyush/Desktop/SIH_TMS/photos/Jadoo.jpeg",
        "landmarks": user_landmarks.get("USR005")
    },
    "USR006": {
        "name": "Piyush Deshmukh",
        "aadhaar": "555566667777",  # store Aadhaar without spaces
        "pan": "PIYUSH5678D",
        "passport": "V1234567",
        "photo": "/home/piyush/Desktop/SIH_TMS/photos/Kaka.jpg",
        "landmarks": user_landmarks.get("USR006")
    }
}


@app.route('/')
def home():
    return jsonify({"message": "Welcome to VigiLocker Prototype API"})


@app.route('/verify', methods=['POST'])
def verify_user():
    data = request.json
    name = data.get("name", "").strip().lower()
    doc_number = normalize_doc(data.get("document_number", ""))
    embeddings = data.get("embeddings")  # dict with left_eye, right_eye, nose, mouth

    print("Received name:", name)
    print("Received document number (normalized):", doc_number)
    print("Received embeddings keys:", list(embeddings.keys()) if embeddings else None)

    if not embeddings:
        return jsonify({"status": "rejected", "reason": "No embeddings received"}), 400

    for user_id, user_data in dummy_users.items():
        if user_data["name"].lower() == name and (
            normalize_doc(user_data["aadhaar"]) == doc_number or
            normalize_doc(user_data["pan"]) == doc_number or
            normalize_doc(user_data["passport"]) == doc_number
        ):
            stored_embeddings = user_data["landmarks"]
            if stored_embeddings:
                similarities = []
                for region in ["left_eye", "right_eye", "nose", "mouth"]:
                    if region in embeddings and region in stored_embeddings:
                        sim = cosine_similarity(
                            [np.array(embeddings[region]).flatten()],
                            [np.array(stored_embeddings[region]).flatten()]
                        )[0][0]
                        similarities.append(sim)

                avg_similarity = np.mean(similarities) if similarities else 0
                print("Calculated similarities:", similarities)
                print("Average similarity:", avg_similarity)

                if avg_similarity > 0.6:
                    return jsonify({
                        "status": "verified",
                        "user_id": user_id,
                        "name": user_data["name"],
                        "similarity": avg_similarity
                    })

    return jsonify({"status": "rejected", "reason": "No matching record or low similarity"}), 400


if __name__ == "__main__":
    app.run(port=5001, debug=True)
