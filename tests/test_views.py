import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from counter.models import AnalysisRecord

@pytest.mark.django_db
def test_counter_view_requires_login(client):
    """If a user is logged in, they should be redirected to the login page."""
    
    # Make sure this matches the urls.py name.
    url = reverse('counter:home')
    response = client.get(url)

    # 302 is the code for a redirect.
    assert response.status_code == 302
    assert '/login/' in response.url

@pytest.mark.django_db
def test_user_cannot_delete_others_history(client):

    # Create two users
    user_a = User.objects.create_user(username='attacker', password='password123')
    user_b = User.objects.create_user(username='victim', password='password123')

    # Create a record that belongs to user b
    record = AnalysisRecord.objects.create(
        user=user_b,
        title="Victim's Private Data",
        original_text="Secret stuff",
        word_count=0
    )

    # Log in as user A
    client.login(username='attacker', password='password123')

    # Try to delete user B's record
    url = reverse('counter:delete_analysis', kwargs={'pk': record.pk})
    response = client.post(url)

    # Assertion - It should either redirect without deletion or return a 
    # 404/Permission denied error.
    assert AnalysisRecord.objects.filter(pk=record.pk).exists() is True
