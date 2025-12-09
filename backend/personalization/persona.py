import json

PROFILE_PATH = "data/persona.json"

default_profile = {
    "role": "student",
    "tone": "detailed",
    "expertise": "beginner"
}

def load_profile():
    try:
        return json.load(open(PROFILE_PATH))
    except:
        return default_profile

def save_profile(profile):
    json.dump(profile, open(PROFILE_PATH, "w"))
