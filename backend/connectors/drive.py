
"""
Drive connector stub (Google Drive, OneDrive, etc).
"""

from typing import Dict, Any

def verify_config(config: Dict[str, Any]) -> bool:
    return bool(config.get("api_key") or config.get("credentials"))

def connect(org_id: str, config: Dict[str, Any]):
    ok = verify_config(config)
    return {"connected": ok, "detail": "Saved drive config" if ok else "Invalid config"}

def list_files(config: Dict[str, Any], folder_id: str = None, limit: int = 100):
    """
    Return placeholder file metadata.
    TODO: integrate Google Drive API / Microsoft Graph here.
    """
    return [
        {"id": "file1", "name": "Policy.docx", "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
        {"id": "file2", "name": "Handbook.pdf", "mimeType": "application/pdf"},
    ]
