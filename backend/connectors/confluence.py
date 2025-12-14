
"""
Confluence connector stub.
"""

from typing import Dict, Any

def verify_config(config: Dict[str, Any]) -> bool:
    return bool(config.get("base_url") and config.get("api_token"))

def connect(org_id: str, config: Dict[str, Any]):
    ok = verify_config(config)
    return {"connected": ok, "detail": "Confluence connector saved" if ok else "Invalid config"}

def fetch_pages(config: Dict[str, Any], limit: int = 50):
    """
    Placeholder: return some sample pages.
    TODO: integrate Confluence REST API (pagination, space filters).
    """
    return [{"id": "123", "title": "Product Spec", "content": "..."}, {"id": "124", "title": "HR Policy", "content": "..."}]
