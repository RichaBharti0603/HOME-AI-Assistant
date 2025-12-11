# backend/personalization/store.py
import os
import json
from datetime import datetime

BASE = os.path.join(os.path.dirname(__file__), "..", "personalization")
os.makedirs(BASE, exist_ok=True)

def profile_path(user_id):
    return os.path.join(BASE, f"{user_id}_profile.json")

def load_profile(user_id):
    path = profile_path(user_id)
    if not os.path.exists(path):
        return {"user_id": user_id, "name": "", "preferences": {}, "history": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_profile(user_id, profile):
    path = profile_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)

def append_history(user_id, role, text):
    profile = load_profile(user_id)
    profile.setdefault("history", []).append({"time": datetime.utcnow().isoformat(), "role": role, "text": text})
    save_profile(user_id, profile)
