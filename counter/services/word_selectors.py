# The '..' means move up one directory level to find the models file
from ..models import AnalysisRecord
from django.db.models import Q
from django.shortcuts import get_object_or_404

def get_user_history(user, search_query=""):
    """Fetches and filters the user's analysis history."""

    records = AnalysisRecord.objects.filter(user=user).order_by('-uploaded_at')
    
    # If the search term exists, filter the results to find matches.
    if search_query:
        records = records.filter(
            # Look for the query in the title or original text.
            Q(title__icontains=search_query) |
            Q(original_text__icontains=search_query)
        )
    # Return either the filtered list or the full history.
    return records

def get_record_for_user(user, pk):
    """Securley fetches a record owned by a specific user."""
    return get_object_or_404(AnalysisRecord, pk=pk, user=user)

def delete_record(record):
    """Encapsulates the deleltion logic."""
    record.delete()