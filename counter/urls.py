from django.urls import path
from .views import(
    counter, 
    word_frequency_chart, 
    export_docx, 
    export_pdf
)

app_name = "counter"

urlpatterns = [
    path("", counter, name="home"),
    path("chart/", word_frequency_chart, name="chart"),
    path("export-pdf/", export_pdf, name="export_pdf"),
    path("export-docx/", export_docx, name="export_docx"),
]