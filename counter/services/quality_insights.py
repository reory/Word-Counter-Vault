import re
from collections import Counter

def analyze_quality(text: str) -> dict:
    
    # Split into sequences.
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Longest sentence
    longest_sentence = max(sentences, key=len) if sentences else ""

    # Words
    words = re.findall(r"\b\w+\b", text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    ttr = round(unique_words / total_words, 3) if total_words else 0

    # Overused words (excluding common stopwords)
    stopwords = {
        "the", "and", "to", "a", "of", "in", "is", "it", 
        "that", "for", "on", "with", "as", "was", "were", 
        "be", "this", "by", "are", "at", "from"
    }
    filtered = [w for w in words if w not in stopwords]
    overused = Counter(filtered).most_common(5)

    # Passive voice detection
    passive_matches = re.findall(r"\b(be|is|was|were|been|being)\s+\w+ed\b", text.lower())
    passive_count = len(passive_matches)

    return {
        "longest_sentence": longest_sentence,
        "ttr": ttr,
        "overused": overused,
        "passive_count": passive_count
    }