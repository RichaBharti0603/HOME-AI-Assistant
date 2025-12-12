import json
import os

PROFILE_PATH = "backend/profile/user_profile.json"


def load_profile():
    if not os.path.exists(PROFILE_PATH):
        return {}
    try:
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_profile(profile_data):
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=4)


def update_profile(field, value):
    profile = load_profile()
    profile[field] = value
    save_profile(profile)
    return profile


def get_active_features(profile):
    """
    Determines the available features based on ownership and context.
    This function only SELECTS features; actual implementations happen elsewhere.
    """

    ownership = profile.get("ownership", "personal")
    context = profile.get("context", "")

    features = {
        "rag": True,  # Always available
        "memory": True,
        "slack_integration": False,
        "file_manager": False,
        "enterprise_connectors": False
    }

    if ownership == "personal":
        features["file_manager"] = True

    if ownership == "enterprise":
        features["slack_integration"] = True
        features["enterprise_connectors"] = True

    # You can refine this later based on context (e.g., finance, healthcare)

    return features
