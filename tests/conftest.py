import pytest
from django.contrib.auth.models import User

from counter.models import AnalysisRecord


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="password123",
    )


@pytest.fixture
def analysis_record(user):
    return AnalysisRecord.objects.create(
        user=user,
        title="Python Analysis",
        original_text="Sample text",
        word_count=3,
        summary="Sample summary",
    )