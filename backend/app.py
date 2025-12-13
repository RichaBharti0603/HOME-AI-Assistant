from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.personalization.store import load_profile, save_profile, append_history
from backend.rag.retriever import get_answer as get_rag_answer
from backend.models.local_llm import generate_streaming_answer
from backend.api.server import app


import time

app = FastAPI(title="HOME AI Assistant API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    user_id: str = None
    stream: bool = False


# ------------------------------
# ONBOARDING ROUTER
# ------------------------------
def onboarding_router(user_id, question, profile):

    # Step 1: identify use-case
    if profile.get("use_case") is None:
        if "personal" in question.lower():
            profile["use_case"] = "personal"
            save_profile(user_id, profile)
            return "Great. What do you want me to help you with personally? (health, productivity, study, notes, etc.)"

        elif "enterprise" in question.lower():
            profile["use_case"] = "enterprise"
            save_profile(user_id, profile)
            return "Understood. Please provide API key or integration file of your organization."

        else:
            return "Are you using this assistant for personal use or enterprise use?"

    # Step 2: personal onboarding
    if profile["use_case"] == "personal" and not profile.get("onboarding_complete"):
        profile["preferences"] = question
        profile["onboarding_complete"] = True
        save_profile(user_id, profile)
        return "Perfect, your preferences are saved. How can I assist you today?"

    # Step 3: enterprise onboarding
    if profile["use_case"] == "enterprise" and not profile.get("onboarding_complete"):
        profile["org_details"] = {"integration_info": question}
        profile["onboarding_complete"] = True
        save_profile(user_id, profile)
        return "Your organization is integrated successfully. How can I assist you?"

    return None



# ------------------------------
# MAIN ROUTER
# ------------------------------
def main_router(user_id, question, profile):

    # If enterprise, we route to org API (stub for now)
    if profile.get("use_case") == "enterprise":
        if "slack" in question.lower():
            return "Slack API integration placeholder."
        if "file" in question.lower():
            return "Enterprise File Manager placeholder."
        # fallback
        return get_rag_answer(question)

    # If personal, use RAG + LLM
    rag_result = get_rag_answer(question)
    return rag_result



# ------------------------------
# STREAMING ENDPOINT
# ------------------------------
@app.post("/ask_stream")
def ask_stream(payload: Query):
    user_id = payload.user_id or "default_user"
    profile = load_profile(user_id)

    onboard_reply = onboarding_router(user_id, payload.question, profile)
    if onboard_reply:
        return StreamingResponse(generate_streaming_answer(onboard_reply), media_type="text/plain")

    answer = main_router(user_id, payload.question, profile)
    return StreamingResponse(generate_streaming_answer(answer), media_type="text/plain")



# ------------------------------
# SYNC ENDPOINT
# ------------------------------
@app.post("/ask")
def ask(payload: Query):
    user_id = payload.user_id or "default_user"
    profile = load_profile(user_id)

    onboard_reply = onboarding_router(user_id, payload.question, profile)
    if onboard_reply:
        return {"answer": onboard_reply}

    answer = main_router(user_id, payload.question, profile)
    return {"answer": answer}
