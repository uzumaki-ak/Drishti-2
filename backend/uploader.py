import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Folder containing scenario files
folder_path = "scene_context"

# Loop through all .json files
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        doc_id = filename.replace(".json", "")  # e.g., scenario_1
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r") as f:
            data = json.load(f)
            db.collection("scene_contexts").document(doc_id).set(data)
            print(f"Uploaded {doc_id}")

print("All files uploaded successfully!")
