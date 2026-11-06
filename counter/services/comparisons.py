from .analysis import get_word_frequencies
from .quality_insights import analyse_quality, get_basic_metrics
from .summariser import generate_summary


def get_comparison_insights(quality_a: dict,quality_b: dict,) -> list:
    """Generate evidence-based comparison observations."""

    # Store human-readable findings for the comparison report
    insights = []
    
    # Compare variety of vocabulary used
    if quality_a["ttr"] > quality_b["ttr"]:
        insights.append(
            "Text A shows greater lexical diversity."
        )
    elif quality_b["ttr"] > quality_a["ttr"]:
        insights.append(
            "Text B shows greater lexical diversity."
        )

    # Compare passive voice usuage.
    if quality_a["passive_count"] < quality_b["passive_count"]:
        insights.append(
            "Text A uses less passive voice."
        )
    elif quality_b["passive_count"] < quality_a["passive_count"]:
        insights.append(
            "Text B uses less passive voice."
        )

    # Compare readability scores
    if quality_a["flesch_score"] > quality_b["flesch_score"]:
        insights.append(
            "Text A is easier to read."
        )
    elif quality_b["flesch_score"] > quality_a["flesch_score"]:
        insights.append(
            "Text B is easier to read."
        )

    return insights


def compare_texts(text_a: str, text_b: str) -> dict:
    """Compare two text submissions and return side-by-side metrics."""

    # Generate baseline stats for both texts
    metrics_a = get_basic_metrics(text_a)
    metrics_b = get_basic_metrics(text_b)

    # Generate readability and quality metrics
    quality_a = analyse_quality(text_a)
    quality_b = analyse_quality(text_b)

    # Generate evidence based comparison observations
    insights = get_comparison_insights(
        quality_a,
        quality_b,
    )

    # Generate summaries and topic extraction
    summary_a = generate_summary(text_a)
    summary_b = generate_summary(text_b)

    # Build a unqiue vocabulary set for Text A
    vocab_a = {
        word for word, _ in get_word_frequencies(text_a, limit=2000)
    }

    # Build a unique vocabulary set for Text B
    vocab_b = {
        word for word, _ in get_word_frequencies(text_b, limit=2000)
    }

    # Calculate shared and unique vocabulary.
    shared_words = sorted(vocab_a & vocab_b)
    unique_to_a = sorted(vocab_a - vocab_b)
    unique_to_b = sorted(vocab_b - vocab_a)

    # Total unique vocabulary across both texts.
    total_vocab = len(vocab_a | vocab_b)

    # Calculate vocabulary overlap percentage.
    overlap_percent = (round((len(shared_words) / total_vocab) * 100, 2)
                        if total_vocab
                        else 0.0
                    )
    return {
        "text_a": {
            "metrics": metrics_a,
            "quality": quality_a,
            "summary": summary_a,
        },
        "text_b": {
            "metrics": metrics_b,
            "quality": quality_b,
            "summary": summary_b,
        },
        "comparison": {
            "shared_words": shared_words,
            "unique_to_a": unique_to_a,
            "unique_to_b": unique_to_b,
            "vocabulary_overlap": overlap_percent,
            "insights": insights,
        },
    }