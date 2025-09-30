from typing import Literal


def categorize_email(text: str) -> Literal["urgent", "action", "info", "spam"]:
    lower = text.lower()
    if any(k in lower for k in ["asap", "urgent", "immediately", "deadline"]):
        return "urgent"
    if any(k in lower for k in ["please review", "could you", "action required", "follow up"]):
        return "action"
    if any(k in lower for k in ["unsubscribe", "free", "win", "lottery", "promo"]):
        return "spam"
    return "info"


def prioritize_score(text: str) -> int:
    score = 0
    lower = text.lower()
    if "ceo" in lower or "vp" in lower or "director" in lower:
        score += 3
    if any(k in lower for k in ["deadline", "today", "end of day", "eod"]):
        score += 2
    if any(k in lower for k in ["customer", "client", "contract"]):
        score += 2
    if "thank you" in lower:
        score += 1
    return max(1, min(10, score))


def summarize_email(text: str) -> str:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    return ". ".join(sentences[:2]) + ("." if sentences else "")


def draft_email_reply(original_text: str, tone: str = "professional") -> str:
    if tone not in {"professional", "friendly", "concise"}:
        tone = "professional"
    openings = {
        "professional": "Hello,",
        "friendly": "Hi there!",
        "concise": "Hi,",
    }
    closing = {
        "professional": "Best regards,\nYour Name",
        "friendly": "Thanks!\nYour Name",
        "concise": "Thanks,\nYour Name",
    }
    body = (
        "Thanks for your message. I have reviewed the details and will follow up "
        "with the next steps. Please let me know if there is anything specific you "
        "would like me to prioritize."
    )
    return f"{openings[tone]}\n\n{body}\n\n{closing[tone]}"


