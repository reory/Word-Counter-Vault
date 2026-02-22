import re
from collections import Counter
from .analysis import STOP_WORDS

def generate_summary(text: str) -> dict:

    # This splits on . ! or ? ONLY if followed by a space.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return {
            "summary": "",
            "bullets": [],
            "topics": []
        }
    
    # Short summary. first 2 sentences.
    summary = " ".join(sentences[:2])

    # Bullet points = first 4 sentences
    bullets = sentences[:4]

    # Topics = Most common words.
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
    
    # Filter using the master STOP_WORDS list.
    filtered = [w for w in words if w not in STOP_WORDS and len(w) > 2]

    # Count frequencies.
    common = Counter(filtered).most_common(5)
    topics = [w for w, _ in common]

    return {
        "summary": summary,
        "bullets": bullets,
        "topics": topics
    }