from django.apps import AppConfig


class CounterConfig(AppConfig):
    """Application configuration for the Counter app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "counter"
