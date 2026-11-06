import pytest
from django.contrib.auth.models import User
from django.http import Http404

from counter.models import AnalysisRecord
from counter.services.word_selectors import (
    delete_record,
    get_record_for_user,
    get_user_history,
)


@pytest.mark.django_db
def test_get_user_history_returns_user_records(user, analysis_record):
    """Verify a user's analysis history is returned."""

    results = get_user_history(user)

    assert results.count() == 1
    assert results.first() == analysis_record



@pytest.mark.django_db
def test_get_user_history_filters_by_search_query(user):
    """Verify records can be filtered by search term."""

    AnalysisRecord.objects.create(
        user=user,
        title="Python Analysis",
        original_text="Text",
        word_count=1,
        summary="Summary",
    )

    AnalysisRecord.objects.create(
        user=user,
        title="Django Analysis",
        original_text="Text",
        word_count=1,
        summary="Summary",
    )

    results = get_user_history(user, "Python")

    assert results.count() == 1
    assert results.first().title == "Python Analysis"


@pytest.mark.django_db
def test_get_record_for_user_returns_owned_record(user, analysis_record):
    """Verify a user can retrieve their own record."""

    result = get_record_for_user(user, analysis_record.pk)

    assert result == analysis_record


@pytest.mark.django_db
def test_delete_record_removes_record(analysis_record):
    """Verify a record is deleted."""

    delete_record(analysis_record)

    assert AnalysisRecord.objects.count() == 0


@pytest.mark.django_db
def test_get_record_for_user_rejects_other_user(user):
    """Verify users cannot access records they do not own."""

    other_user = User.objects.create_user(
        username="other",
        password="password123",
    )

    record = AnalysisRecord.objects.create(
        user=other_user,
        original_text="Text",
        word_count=1,
        summary="Summary",
    )

    with pytest.raises(Http404):
        get_record_for_user(user, record.pk)