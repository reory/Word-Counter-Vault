from collections import Counter
import re

def get_word_frequencies(text: str, limit: int = 10):

    # Lowercase and extract words.
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())

    # Count frequencies.
    counter = Counter(words)

    # Return the top N words.
    return counter.most_common(limit)
