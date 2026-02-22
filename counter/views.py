from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from typing import Any
from .services.text_extractors import get_text_from_uploaded_file
from .services.summarizer import generate_summary
from .services.quality_insights import analyze_quality, get_basic_metrics
from .services import exporters, word_selectors
from .models import AnalysisRecord
import duckdb
import os
import re


# A "decorator" that forces the user to log in before they can access this view.
# User will not see this view until they are logged-in. 
@login_required 
def counter(request):
    
    """Main view."""
    context: dict[str, Any] = {"on": "active"}
    
    # Check if we have text from a previous redirect or current session.
    text = request.session.get("analysis_text", "")
    if request.method == "POST":
        
        # Text from text area.
        text = request.POST.get("texttocount", "")
        
        # Text from file upload.
        if "file" in request.FILES:
            uploaded_file = request.FILES["file"]

            # 1. DELEGATE TO EXTRACTOR SERVICE
            text = get_text_from_uploaded_file(uploaded_file)

            if text:
                messages.success(request, f"'{uploaded_file.name}' analyzed successfully!")
            else:
                messages.error(request, f'Unsupported file type: {uploaded_file.name}')
                return redirect('counter:home')              
                
        # Reset the save guard for the new data.
        request.session['is_saved'] = False

        # Store text in session and redirect.
        request.session["analysis_text"] = text
        return redirect("counter:home")
        
    # Analysis metrics. (Runs on GET after redirect.)
    if text:
        # 2. DELEGATE LINGUISTIC MATH TO SERVICES
        metrics = get_basic_metrics(text)
        summary_data = generate_summary(text)
        quality_data = analyze_quality(text)

        # Hook up the DuckDB.

        # Lowercase the text and remove everything except letters/numbers. 
        clean_text = text.lower()
        # regex finds only letters and ignores commas, periods, etc.
        words_only = re.findall(r'\b\w+\b', clean_text)
        # use set() to get unique words only (faster for Duckdb)
        all_unique_words = list(set(words_only))
        # Check the vault for all these words.
        vault_pins = get_value_matches(all_unique_words)
        
        # Update context cleanly
        context.update(metrics) # Adds word_count, sentence_count, paragraph_count, etc.
        context.update({
            "text": text,"has_result": True,
            "vault_pins": vault_pins,
            "show_chart": len(text) < 30000,
            "summary": summary_data["summary"],"bullets": summary_data["bullets"],
            "topics": summary_data["topics"],
            "longest_sentence": quality_data["longest_sentence"],
            "ttr": quality_data["ttr"],"overused": quality_data["overused"],
            "passive_count": quality_data["passive_count"]
        })

        # Save details of the logged in user into the database.
        if request.user.is_authenticated:
            if not request.session.get("is_saved"):
                
                record_title = "Manual Entry"
                if "file" in request.FILES:
                    record_title = request.FILES["file"].name

                AnalysisRecord.objects.create(
                    user=request.user,title=record_title,original_text=text,
                    word_count=metrics['word_count'], # Extracted from metrics dictionary
                    summary=summary_data['summary'],topics=summary_data['topics'],
                    bullets=summary_data['bullets'],
                    longest_sentence=quality_data['longest_sentence'],
                    ttr=quality_data['ttr'],overused=quality_data['overused'],
                    passive_count=quality_data['passive_count']
                )
                # Mark as saved so a refresh does not duplicate the entry.
                request.session['is_saved'] = True

        # Save everything to session for a PDF export.
        for key in ["summary", "bullets", "topics", "word_count", 
                    "longest_sentence", "ttr", "overused", "passive_count"]:
            request.session[key] = context.get(key)  
    return render(request, "counter/counter.html", context)

def register(request):
    """A registration form for a user details to be saved to the DB.."""

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Save the new user to the database.
            form.save()
            # Get the username to personalize the success message.
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}! Please log in.')
            return redirect('login')
        
    else:
        # If they are just visiting the page, show an empty form.
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def export_docx(request, pk=None):
    """
    Export the PDF document for the user, either from the current session
    or the vault (database).
    """
    # 1. Gather data using the coordinator
    data = exporters.get_export_data(request.user, pk, request.session)

    # 2. Generate and return
    docx_bytes = exporters.generate_docx_report(data)
    response = HttpResponse(docx_bytes, 
                            content_type="application/vnd.openxmlformats-"
                            "officedocument.wordprocessingml.document")
    response["Content-Disposition"] = "attachment; filename=analysis_report.docx"
    return response


def export_pdf(request, pk=None):
    """Export the WORD document for the user."""

    # Gather data using the coordinator
    data = exporters.get_export_data(request.user, pk, request.session)
    data[
        'logo_url'] = request.build_absolute_uri(static(
            'counter/img/python_developer.png'))
    
    # Generate and return
    pdf_bytes = exporters.generate_pdf_report(data)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=analysis_report.pdf'
    return response

def word_frequency_chart(request):
    """
    A thin wrapper that fetches text from the URL 
    and returns a PNG from the service layer.
    """
    text = request.GET.get("text", "")
    if not text.strip():
        return HttpResponse("No text provided", status=400)
    
    # We use the existing chart logic now moved to exporters or a visuals service
    chart_bytes = exporters.generate_word_frequency_chart_image(text)
    
    return HttpResponse(chart_bytes.getvalue(), content_type="image/png")

@login_required
def history(request):
    """
    Fetches all analysis records for the current user,
    ordered by newest first.
    """
    query = request.GET.get('q', "")
    records = word_selectors.get_user_history(request.user, query)
    return render(request, 'counter/history.html', {'records': records})
    
@login_required
def history_detail(request, pk):
    """
    Fetches a specific analysis record by its primary key (pk)
    Ensures the record belongs to the logged-in user.
    """
    record = word_selectors.get_record_for_user(request.user, pk)
    return render(request, 'counter/analysis_detail.html', {'record': record})

@login_required
def delete_analysis(request, pk):
    # Fetch the record or 404 if it doesn't exist/or belong to the user.

    # Fetch the specific record, 
    # ensuring it actually belongs to the current user
    record = word_selectors.get_record_for_user(request.user, pk)
    # Only proceed with deletion if the user explicitly submitted a form (POST)
    if request.method == 'POST':
        word_selectors.delete_record(record)
        messages.success(request, 'Record deleted successfully!')
    # Send the user back to the history list regardless of the outcome
    return redirect("counter:history")

def get_value_matches(word_list):
    """Connects to DuckDB and returns a list of dictionaries
    for words that exist in our "origins" table"""

    db_path = os.path.join(settings.BASE_DIR, 'word_vault_analytics.duckdb')

    # We use a context manager to handle the connection safely.
    with duckdb.connect(db_path, read_only=True) as con:
        # Lets us pass a python list directly.
        results = con.execute("""
            SELECT word, root, country, lat, lng, fact
            FROM origins
            WHERE word IN ?
        """, [word_list]).fetchall()

    # Turn the raw tuples into a clean list of dicts for our JS map.
    return [
        {
            'word': r[0],
            'root': r[1],
            'country': r[2],
            'lat': r[3],
            'lng': r[4], 
            'fact': r[5]       
        } for r in results
    ]

