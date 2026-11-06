from io import BytesIO
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from counter.models import AnalysisRecord


@pytest.mark.django_db
def test_counter_view_requires_login(client):
    """If a user is not logged in, they should be redirected to login."""

    # Resolve the homepage URL from urls.py.
    url = reverse("counter:home")
    response = client.get(url)

    # Anonymous users should be redirected by @login_required.
    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_user_cannot_delete_others_history(client):
    """Verify users cannot delete analysis records owned by others."""

    # Create two separate users.
    User.objects.create_user(
        username="attacker",
        password="password123",
    )
    user_b = User.objects.create_user(
        username="victim",
        password="password123",
    )

    # Create a record belonging to the victim account.
    record = AnalysisRecord.objects.create(
        user=user_b,
        title="Victim's Private Data",
        original_text="Secret stuff",
        word_count=0,
    )

    # Authenticate as the attacker.
    client.login(
        username="attacker",
        password="password123",
    )

    # Attempt to delete another user's record.
    url = reverse(
        "counter:delete_analysis",
        kwargs={"pk": record.pk},
    )
    client.post(url)

    # The record should still exist after the request.
    assert AnalysisRecord.objects.filter(pk=record.pk).exists() is True


@pytest.mark.django_db
def test_register_page_loads(client):
    """Verify the registration page loads."""

    # Request the registration form.
    response = client.get("/register/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_can_register(client):
    """Verify a user can create an account."""

    # Submit a valid registration form.
    response = client.post(
        "/register/",
        {
            "username": "newuser",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        },
    )

    # Successful registration redirects the user.
    assert response.status_code == 302


@pytest.mark.django_db
def test_history_page_loads(client, user):
    """Verify the history page loads."""

    # Access requires authentication.
    client.force_login(user)

    response = client.get("/history/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_history_page_search(client, user):
    """Verify history can be filtered by query string."""

    # Log in before accessing the history view.
    client.force_login(user)

    # Submit a search query through the URL.
    response = client.get(
        "/history/",
        {"q": "python"},
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_history_detail_loads(client, user, analysis_record):
    """Verify an analysis detail page loads."""

    # Ensure the user owns the requested record.
    client.force_login(user)

    response = client.get(
        f"/history/{analysis_record.pk}/"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_analysis(client, user, analysis_record):
    """Verify a record can be deleted."""

    client.force_login(user)

    # Submit the delete request.
    response = client.post(
        f"/history/delete/{analysis_record.pk}/"
    )

    # Users are redirected after deletion.
    assert response.status_code == 302

    # The record should no longer exist in the database.
    assert AnalysisRecord.objects.count() == 0


@pytest.mark.django_db
def test_clear_history(client, user):
    """Verify all user records can be deleted."""

    client.force_login(user)

    # Create a record to be cleared.
    AnalysisRecord.objects.create(
        user=user,
        original_text="Text",
        word_count=1,
        summary="Summary",
    )

    response = client.post("/history/clear/")

    # View redirects after clearing the vault.
    assert response.status_code == 302

    # All records owned by the user should be removed.
    assert AnalysisRecord.objects.count() == 0


@pytest.mark.django_db
def test_word_frequency_chart_requires_text(client):
    """Verify the chart view rejects empty input."""

    # Call the endpoint without a text parameter.
    response = client.get("/chart/")

    assert response.status_code == 400
    assert b"No text provided" in response.content


@patch("counter.views.exporters.generate_word_frequency_chart_image")
def test_word_frequency_chart_success(mock_chart,client,):
    """Verify chart images are returned."""

    # Mock chart generation so no real image processing occurs.
    mock_chart.return_value = BytesIO(b"fake_png")

    response = client.get(
        "/chart/",
        {"text": "python python django"},
    )

    # The endpoint should return PNG image data.
    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
