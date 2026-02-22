import pytest
from counter.services.analysis import get_word_frequencies

def test_get_word_frequencies_basic():

    text = "The quick brown fox jumps over the lazy dog."

    # The - is a stop word, so it should be filtered out.
    results = get_word_frequencies(text)
    
    words = [word for word, count in results]
    assert "quick" in words
    assert "the" not in words

def test_get_word_frequencies_punctuation():

    text = "Code, code, and more code!"

    # Should handle commas and excamation marks via the regex.
    results = get_word_frequencies(text)

    word, count = results[0] # "code" should be the most common.
    assert word == "code"
    assert count == 3

def test_get_word_frequencies_limit():

    text = 'two four six eight ten'

    # Testing the limiting parameter
    results= get_word_frequencies(text, limit=2)
    assert len(results) == 2
