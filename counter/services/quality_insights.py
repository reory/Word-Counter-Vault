import re
from collections import Counter
from .analysis import STOP_WORDS

def get_basic_metrics(text: str) -> dict:
    """Calculates core counters and reading time."""

    # Ensure new lines don't blesd titles into sentences
    clean_text = text.replace('\n', ', ')
    
    # Split the string by whitespace into a list and count the items (words)
    word_count = len(text.split())
    # Count every individual character in the string, including spaces and punctuation
    char_count = len(text)

    # Sentence detection logic.
    sentence_count = (clean_text.count('.') +
                      clean_text.count('!') +
                      clean_text.count('?'))

    # Paragraph detection
    paragraph_count = len([p for p in text.split('\n') if p.strip()])

    # Reading time (Standard 200 wpm)
    reading_time = max(1, round(word_count / 200))

    return {
        "word_count": word_count,
        "char_count": char_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "reading_time": reading_time,
    }

def analyze_quality(text: str) -> dict:
    
    # Split into sequences.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Longest sentence
    longest_sentence = max(sentences, key=len) if sentences else ""

    # Words
    words = re.findall(r"\b\w+\b", text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    ttr = round(unique_words / total_words, 3) if total_words else 0

    # Overused words (Using the import STOP_WORDS)
    filtered = [w for w in words if w not in STOP_WORDS]
    
    # We only want words used more than 3 times to count as overused words
    overused = [item for item in Counter(filtered).most_common(5) if item[1] > 3]

    # Passive voice/count detection
    passive_matches = re.findall(r"\b(be|is|was|were|been|being)\s+\w+(ed|en)\b", text.lower())
    passive_count = len(passive_matches)

    return {
        "longest_sentence": longest_sentence,
        "ttr": ttr,
        "overused": overused,
        "passive_count": passive_count
    }