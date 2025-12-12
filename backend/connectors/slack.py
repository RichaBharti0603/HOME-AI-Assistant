# backend/connectors/slack.py
"""
Slack connector stub.

Replace placeholders with real slack-sdk usage or HTTP calls.
"""

from typing import Dict, Any

def verify_config(config: Dict[str, Any]) -> bool:
    """
    Basic validation of connector config (token present, etc).
    """
    token = config.get("bot_token") or config.get("token")
    return bool(token)

def connect(org_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save connector config to your org profile (or secrets manager).
    TODO: secure storage, token validation, OAuth flow.
    """
    # Example validation
    ok = verify_config(config)
    return {"connected": ok, "detail": "Saved config" if ok else "Invalid config"}

def fetch_recent_messages(config: Dict[str, Any], channel: str = None, limit: int = 50):
    """
    Placeholder: return sample messages for indexing.
    TODO: call Slack API (conversations.history, users.info etc.)
    """
    return [
        {"user": "U123", "text": "Sample message 1 from Slack", "ts": "1600000000.0001"},
        {"user": "U456", "text": "Sample message 2 from Slack", "ts": "1600000001.0002"},
    ]
