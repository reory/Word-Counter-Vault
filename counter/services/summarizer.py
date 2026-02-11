def generate_summary(text: str) -> dict:

    # Split into sentences.
    sentences = [s.strip() for s in text.split(".") if s.strip()]

    if not sentences:
        return {
            "summary": "",
            "bullets": [],
            "topics": []
        }
    
    # Short summary. first 2 sentences - fallback to 1
    summary = " . ".join(sentences[:2]) + "."

    # Bullet points = first 4 sentences
    bullets = [s + "." for s in sentences[:4]]

    # Topics = Most common words (simply heuristic)
    words = text.lower().split()
    stopwords = {"the", "and", "to", "a", "of", 
                 "in", "is", "it", "that", "for", "on", "with"}
    filtered = [w for w in words if w not in stopwords and len(w) > 3]

    # Count frequencies.
    from collections import Counter
    common = Counter(filtered).most_common(5)
    topics = [w for w, _ in common]

    return {
        "summary": summary,
        "bullets": bullets,
        "topics": topics
    }