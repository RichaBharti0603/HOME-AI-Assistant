from backend.tools.slack import slack_search
from backend.tools.files import file_lookup

def route_tool_call(question, profile):
    q = question.lower()

    if "slack" in q:
        return slack_search(q)

    if "file" in q or "document" in q:
        return file_lookup(q)

    return None
