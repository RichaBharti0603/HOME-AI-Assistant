from backend.models.local_llm import run_llm

SUMMARY_PROMPT = """
Summarize the following conversation briefly.
Preserve important facts, names, and preferences.

Conversation:
{conversation}

Summary:
"""


def summarize_conversation(text: str) -> str:
    prompt = SUMMARY_PROMPT.format(conversation=text)
    return run_llm(prompt)
