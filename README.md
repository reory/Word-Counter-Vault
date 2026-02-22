# 📚 Word Counter Vault — Full-Stack Linguistic Analysis Suite

An interactive intelligence dashboard and automated reporting tool built to analyze linguistic patterns and global etymology. This project transforms raw text input into actionable forensic insights using a modern Python stack.

## 🎥 Project Walkthrough
[![Watch the Demo on LinkedIn](https://img.shields.io/badge/LinkedIn-Video_Walkthrough-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/posts/roy-p-74980b382_python-django-datascience-ugcPost-7431321183679045632-peek?utm_source=share&utm_medium=member_desktop&rcm=ACoAAF5yzmkBKYhDCqFaGGMG8mt7ntE88OY67k8)

> **Note:** Click the badge above to view the full feature walkthrough and linguistic analysis demo on LinkedIn.

---

## 📸 Screenshots
See the full gallery here:
<details>
 <summary><b>Click to expand screenshots</b></summary>
 <br>

 ![Main Dashboard](screenshots/user_UI.png)
 ![Main Dashboard](screenshots/user_UI2.png)
 ![Main Dashboard Map](screenshots/map_of_words_history.png)
 ![Main Dashboard Map](screenshots/map.png)
 ![Main Login](screenshots/login_view.png)
 ![PDF Report](screenshots/pdf_report.png)
 ![Word Document](screenshots/word_document.png)
 ![Chart View](screenshots/chart.png)
 ![Indepth UI](screenshots/indepth_UI.png)
 ![Main Dashboard](screenshots/analysis_history.png)
 ![View Delete Buttons](screenshots/view_delete_buttons.png)
</details>

---

## 🛠️ Project Architecture
This project is divided into two main components to balance real-time user interaction with deep-dive analytical processing:

---

### 1. Interactive Analysis Dashboard (`views.py` & `templates/`)
The **"Frontend"** logic of the project. It provides a real-time interface for users to explore their text data.
* **Dynamic Geospatial Mapping:** Visualizes the "geographic DNA" of a text by pinpointing word origins across a global map using **Folium**.
* **Instant Linguistic KPIs:** Calculates Lexical Diversity (TTR), Overused Words, and Passive Voice detection on the fly.
* **User Vault:** A persistent history system allowing users to search, review, and manage their analysis records securely.

--- 

### 2. Forensic Reporting & Data Engine (`services/` & `models.py`)
The **"Analytical Backend."** This handles the heavy lifting of data management and document generation.
* **Dual-State Storage:** Manages persistent user history in **SQLite** while offloading high-speed etymological lookups to a **DuckDB** OLAP engine.
* **Global Etymology Pipeline:** A custom ingestion layer that maps over 500+ words to global coordinates (Latin, Germanic, Arabic, Sanskrit, and more).
* **Automated Document Generation:** Compiles findings into professional PDF reports (via **WeasyPrint**) and Word documents (**python-docx**) for offline review.

---

## 📁 File Structure
* `word_counter/settings.py`: Core configuration for the Django environment.
* `counter/views.py`: Logic for text processing, regex normalization, and dashboard rendering.
* `counter/services/seed_origins.py`: Data pipeline script for ingesting the global word library.
* `counter/services/word_data.json`: The "Source of Truth" containing 500+ global etymology records.
* `word_vault_analytics.duckdb`: High-performance database for geospatial word lookups.

---

## 🧰 Tech Stack
* **Python 3.10** (Development Environment)
* **Django 5.2:** For the web framework and user authentication.
* **DuckDB:** For high-performance, local analytical etymology queries.
* **SQLite:** For persistent user history and session management.
* **Folium/Leaflet:** For interactive geospatial mapping.
* **WeasyPrint / python-docx:** For automated forensic report creation.
* **Regex:** For high-speed text normalization and cleaning.

---

## ⚙️ Installation & Local Usage
To run this project locally:
1. **Clone the repo:** `git clone https://github.com/reory/Word-Counter-Vault.git`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Seed the Global Vault:** `python -m counter.services.seed_origins`
4. **Launch the app:** `python manage.py runserver`

---

## 🧪 Quality Assurance & Testing
This project implements a comprehensive automated testing suite using **Pytest** to ensure data integrity and security across the analytical pipeline.

### Test Coverage:
* **Linguistic Logic:** Validates regex normalization, word frequency calculations, and lexical diversity metrics.
* **Security & Permissions:** Ensures strict object-level access control (e.g., users cannot view or delete others' analysis history).
* **Service Layer & Mocking:** Utilizes `pytest-mock` to simulate **DuckDB** OLAP connections, allowing for high-speed testing without disk I/O dependency.
* **File Extraction:** Verifies robust handling of `.txt`, `.pdf`, and `.docx` uploads using Django's `SimpleUploadedFile`.

### Running Tests locally:
```bash
pytest
```

## 🙏 Acknowledgments
* **Etymology Sources:** Online Etymology Dictionary for root-word tracking.
* **Community:** Thanks to the Django and DuckDB communities for the robust library support.

---

## 🛣️ Roadmap

- [x] **Core Architecture:** Dual-Engine (Django + DuckDB) setup.
- [ ] **Data Seeding:** Integration with `Faker` for large-scale stress testing.
- [ ] **Geospatial Mapping:** Interactive etymology origins via Plotly/Mapbox.
- [x] **Forensic Reporting:** PDF/CSV export functionality for text analysis.
- [x] **User Accounts:** Private storage for linguistic history.

---

## ⚖️ License
This project is licensed under the MIT License - see the `LICENSE` file for details.

---

**Built By Roy Peters** [Click here for contact info 😁](https://www.linkedin.com/in/roy-p-74980b382/)
