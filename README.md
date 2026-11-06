# 📚 Word Counter Vault — Full-Stack Linguistic Analysis Suite

<p align="center">

  <img src="https://img.shields.io/github/last-commit/reory/Word-Counter-Vault?style=for-the-badge" />
  <img src="https://img.shields.io/github/repo-size/reory/Word-Counter-Vault?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" />

---

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=leaflet&logoColor=white" />
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=000000" />

</p>

An interactive intelligence dashboard and automated reporting tool built to analyse linguistic patterns and global etymology. This project transforms raw text input into actionable forensic insights using a modern Python stack.

---

## 📑 Table of Contents

- [Why This Project Was Built](#-why-this-project-was-built)
- [Project Walkthrough](#-project-walkthrough)
- [Screenshots](#-screenshots)
- [Project Architecture](#-project-architecture)
- [File Structure](#-file-structure)
- [Tech Stack](#-tech-stack)
- [Installation & Local Usage](#️-installation--local-usage)
- [Stress Testing & Database Seeding](#-stress-testing--database-seeding)
- [Quality Assurance & Testing](#-quality-assurance--testing)
- [Acknowledgments](#-acknowledgments)
- [Roadmap Features](#️-roadmap-features)

---

## 🧠 Why This Project Was Built

This project was built to explore text analysis beyond simple word counts. It combines linguistic analysis, readability scoring, word origins, geospatial visualisation, and automated reporting into a single application, while serving as a practical showcase of modern Python and Django development.

---

## 🎥 Project Walkthrough

<details>
  <summary>Click here</summary>

[![Watch the Demo on LinkedIn](https://img.shields.io/badge/LinkedIn-Video_Walkthrough-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/posts/roy-p-74980b382_python-django-datascience-ugcPost-7431321183679045632-peek?utm_source=share&utm_medium=member_desktop&rcm=ACoAAF5yzmkBKYhDCqFaGGMG8mt7ntE88OY67k8)

> **Note:** Click the badge above to view the full feature walkthrough and linguistic analysis demo on LinkedIn.

</details>

---

## 📸 Screenshots

See the full gallery here:

<details>
  <summary><b>Click to expand screenshots</b></summary>
  <br>

- Analysis view after inputting text into the text box
 ![Main Dashboard](screenshots/user_UI.png)
 ![Main Dashboard](screenshots/user_UI2.png)
---
- Geographic map of where words originate from.
 ![Main Dashboard Map](screenshots/map_of_words_history.png)
 ![Main Dashboard Map](screenshots/map.png)
---
- login view screen
 ![Main Login](screenshots/login_view.png)
---
- PDF report
 ![PDF Report](screenshots/pdf_report.png)
- Word document report
 ![Word Document](screenshots/word_document.png)
---
- Top ten most common words identified from the text input
 ![Chart View](screenshots/chart.png)
---
- In Depth view of entered text
 ![In-Depth UI](screenshots/indepth_UI.png)
---
 - Text Analysis history view
 ![Main Dashboard](screenshots/analysis_history.png)
---
 - Delete Buttons
 ![View Delete Buttons](screenshots/view_delete_buttons.png)
---
 - Readability Score Guide 
 - Flesch Reading Ease (0–100 scale):
 High score: Easy to read (plain English, blogs, general audiences).
 Low score: Very difficult (dense academic or legal texts).
- Gunning Fog Index (Years of education required):
High score: Advanced professional/college level (requires 16+ years of education).
Low score: Mass-market, accessible level (high school or below).
 ![Flesch_score & Gunning_fog](screenshots/flesch_score_gunning_fog.png)

</details>

---

## 📁 Project Architecture

```plaintext
Word-Counter-Vault/
│
├── manage.py                    # Django entry point
├── pyproject.toml               # Project dependencies and configuration
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Example environment variables
├── README.md
├── CONTRIBUTING.md
├── LICENSE
│
├── wordcounterapp/              # Django project configuration
│   ├── __init__.py
│   ├── settings.py              # Global settings
│   ├── urls.py                  # Root URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── counter/                     # Main application
│   │
│   ├── models.py                # Database models
│   ├── views.py                 # Request handlers
│   ├── urls.py                  # App URL routes
│   ├── admin.py
│   ├── apps.py
│   └── tests.py
|   |
│   ├── management/
|   |    ├── commands/
│   |        └── seed_stress_data.py
|   |
|   |
│   ├── migrations/              # Django database migrations
│   │   ├── 0001_initial.py
│   │   └── 0002_analysisrecord_bullets_and_more.py
│   │
│   ├── services/                # Business logic layer
│   │   ├── analysis.py
│   │   ├── exporters.py
│   │   ├── quality_insights.py
│   │   ├── summariser.py
│   │   ├── text_extractors.py
│   │   ├── word_selectors.py
│   │   ├── seed_origins.py
│   │   └── word_data.json
│   │
│   ├── templates/               # HTML templates
│   │   │
│   │   ├── counter/
│   │   │   ├── base.html
│   │   │   ├── counter.html
│   │   │   ├── history.html
│   │   │   └── analysis_detail.html
│   │   │
│   │   ├── registration/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   │
│   │   └── export/
│   │       └── pdf_template.html
│   │
│   └── static/
│       └── counter/
│           ├── css/             # Dashboard styling
│           └── img/             # UI assets
│
├── tests/                       # Pytest test suite
│   ├── conftest.py
│   ├── test_analysis.py
│   ├── test_exporters.py
|   ├── test_extractors.py
|   ├── test_quality_insights.py
|   ├── test_seed_origins.py
|   ├── test_summariser.py
|   ├── test_text_extractors.py
|   ├── test_vault.py
|   ├── test_views.py
│   └── test_word_selectors.py
│
├── screenshots/                 # README screenshots
│   ├── user_UI.png
│   ├── user_UI2.png
│   ├── chart.png
│   ├── map.png
│   ├── pdf_report.png
│   └── ...
│
└── analysis/                    # Generated analysis artifacts
    ├── metadata.json
    ├── hashes.json
    └── remaining/
```

---

## 📁 File Structure

* `word_counter/settings.py`: Core configuration for the Django environment.
* `counter/views.py`: Logic for text processing, regex normalisation, and dashboard rendering.
* `counter/services/seed_origins.py`: Data pipeline script for ingesting the global word library.
* `counter/services/word_data.json`: The "Source of Truth" containing 500+ global etymology records.
* `word_vault_analytics.duckdb`: High-performance database for geospatial word lookups.

---

## 🧰 Tech Stack

* **Python 3.12** (Development Environment)
* **Django 5.2:** For the web framework and user authentication.
* **DuckDB:** For high-performance, local analytical etymology queries.
* **SQLite:** For persistent user history and session management.
* **Folium/Leaflet:** For interactive geospatial mapping.
* **WeasyPrint / python-docx:** For automated forensic report creation.
* **Regex:** For high-speed text normalisation and cleaning.

---

## ⚙️ Installation & Local Usage

To run this project locally:

1. **Clone the repo:** `git clone https://github.com/reory/Word-Counter-Vault.git`
2. **Install dependencies:** `uv sync`
3. **Seed the Global Vault:** `python -m counter.services.seed_origins`
4. **Launch the app:** `python manage.py runserver`

---

## 🧪 Stress Testing & Database Seeding

This project includes a custom Django management command powered by **Faker** to generate synthetic `AnalysisRecord` entries for performance and load testing.

### Running the Seeder

To populate your local vault with synthetic records, run:

```bash
python manage.py seed_stress_data --count 500
```

## 🧪 Quality Assurance & Testing

This project implements a comprehensive automated testing suite using **Pytest** to ensure data integrity and security across the analytical pipeline.

### Test Coverage:

* **Linguistic Logic:** Validates regex normalisation, word frequency calculations, and lexical diversity metrics.
* **Security & Permissions:** Ensures strict object-level access control (e.g., users cannot view or delete others' analysis history).
* **Service Layer & Mocking:** Utilises `pytest-mock` to simulate **DuckDB** OLAP connections, allowing for high-speed testing without disk I/O dependency.
* **File Extraction:** Verifies robust handling of `.txt`, `.pdf`, and `.docx` uploads using Django's `SimpleUploadedFile`.

### Running Tests Locally:

```bash
pytest
```

---

## 🙏 Acknowledgments

* **Etymology Sources:** Online Etymology Dictionary for root-word tracking.
* **Community:** Thanks to the Django and DuckDB communities for the robust library support.

---

## 🛣️ Roadmap Features

- [x] **Core Architecture:** Dual-Engine (Django + DuckDB) setup.
- [x] **Forensic Reporting:** PDF/WORD export functionality for text analysis.
- [x] **User Accounts:** Private storage for linguistic history.
- [x] **Data Seeding:** Integration with `Faker` for large-scale stress testing.
- [x] **Readability Metrics:** Add Flesch Reading Ease, and Gunning Fog Index calculations for deeper writing quality assessment.
- [x] **Comparative Analysis:** Compare two text submissions side-by-side to identify differences in vocabulary, lexical diversity, readability, and writing style.
- [ ] **Custom Stopword Management:** Allow users to create personal stopword lists to exclude common or domain-specific words from analysis results.
- [ ] **Analysis Tags & Collections:** Enable users to organiae saved analyses into categories, folders, or tagged collections for improved vault management.
- [ ] **Interactive Word Trends:** Track frequently used words across a user's analysis history to visualise vocabulary evolution over time.
- [ ] **Enhanced Geospatial Mapping:** Interactive etymology origins via `Plotly/Mapbox`.

---

**Built By Roy Peters** 😁 [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/roy-p-74980b382/)
