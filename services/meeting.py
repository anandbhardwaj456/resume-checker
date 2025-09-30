from typing import List


def summarize_transcript(transcript: str) -> str:
    lines = [l.strip() for l in transcript.splitlines() if l.strip()]
    if not lines:
        return ""
    first = lines[0][:200]
    last = lines[-1][:200] if len(lines) > 1 else ""
    return (
        "Meeting covered key topics. Initial discussion: "
        f"{first}. Final notes: {last}."
    )


def extract_action_items(transcript: str) -> List[str]:
    lowered = transcript.lower()
    items: List[str] = []
    for marker in ["action:", "todo:", "next:", "follow-up:"]:
        start = 0
        while True:
            idx = lowered.find(marker, start)
            if idx == -1:
                break
            end = lowered.find("\n", idx)
            snippet = transcript[idx : end if end != -1 else len(transcript)]
            cleaned = snippet.split(":", 1)[-1].strip()
            if cleaned:
                items.append(cleaned)
            start = idx + len(marker)
    if not items:
        items.append("Assign owners and deadlines to key tasks discussed.")
    return items[:10]


