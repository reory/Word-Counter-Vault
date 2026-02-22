from django.urls import path
from . import views

app_name = "counter"

urlpatterns = [
    path("", views.counter, name="home"),
    path("chart/", views.word_frequency_chart, name="chart"),
    # This path is for the homepage.
    path("export-pdf/", views.export_pdf, name="export_pdf"),
    #This path is for the vault history detail page.
    path("export-pdf/<int:pk>/", views.export_pdf, name="export_pdf_by_id"),
    # This path is for the homepage.
    path("export-docx/", views.export_docx, name="export_docx"),
    # This path is for the vault history detail page
    path("export-docx/<int:pk>/", views.export_docx, name="export_docx_by_id"),
    path("history/", views.history, name='history'),
    path("history/<int:pk>/", views.history_detail, name="history_detail"),
    # This path is for the delete button. very important!
    path("history/delete/<int:pk>/", views.delete_analysis, name="delete_analysis"),
    # This path is for the registration page when a user want to sign up.
    path('register/', views.register, name='register')
]