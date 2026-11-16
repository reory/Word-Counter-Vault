from django.contrib.auth.models import User
from django.db import models


class AnalysisRecord(models.Model):
    """Link the analysis to a specific user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="analyses")

    # Store the input.
    title = models.CharField(max_length=255, blank=True)
    original_text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="user_document/%Y/%m/%d/", blank=True, null=True)

    # Store the metrics. (saves recalculating every time.)

    # Counts the number of words.
    word_count = models.IntegerField()

    # Produces a summary of the text.
    summary = models.TextField()

    # Stores the list of topics.
    topics = models.JSONField(default=list)

    # A database column for decimal numbers; 'null=True' allows it to be empty
    quality_score = models.FloatField(null=True)

    # Stores the bullet points
    bullets = models.JSONField(default=list, blank=True)

    # Stores the text of the longest sentence
    longest_sentence = models.TextField(blank=True, null=True)

    # Type-Token Ratio (0.0 to 1.0)
    ttr = models.FloatField(default=0.0)

    # Stores [('word', 10), ('word2', 5)]
    overused = models.JSONField(default=list, blank=True)

    # How many passive sentences?
    passive_count = models.IntegerField(default=0)

    # Flesch Reading Ease score
    flesch_score = models.FloatField(default=0.0)
    
    # Gunning Fog index for readability
    gunning_fog = models.FloatField(default=0.0)

    def __str__(self):
        """Defines how a object appears as a string."""

        return f"{self.user.username} - {self.title or 'Unnamed'} ({self.uploaded_at.date()})"


class CustomStopword(models.Model):
    """Stores user-defined stopwords to exclude from the text analysis."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="custom_stopwords")
    word = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "word")
        ordering = ("word",)

    def save(self, *args, **kwargs):
        """Normalise word to lowercase and strip whitespace before saving."""

        self.word = self.word.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.user.username} - {self.word}"
