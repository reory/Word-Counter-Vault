# 🤝 Contributing to Word Counter Vault

Thank you for your interest in contributing.

Word Counter Vault is designed to be a practical text-analysis platform that combines linguistic intelligence, readability analysis, etymology research, geospatial visualisation, and automated reporting.

Contributions that improve reliability, usability, performance, testing, documentation, and roadmap features are always welcome.

---

## ⚒️ Getting Started

### Clone the Repository

```bash
git clone https://github.com/reory/Word-Counter-Vault.git
cd Word-Counter-Vault
```

### Install Dependencies

```bash
uv sync
```

### Seed the Global Vault

```bash
python -m counter.services.seed_origins
```

### Run the Application

```bash
python manage.py runserver
```

### Run the Test Suite

```bash
pytest
```

---

## 🧩 Contribution Guidelines

Please keep contributions:

- Small and focused
- Well documented
- Consistent with the existing code style
- Backed by tests where practical
- Aligned with the project's goals

### ✅ Good Contributions

- Bug fixes
- New tests
- Documentation improvements
- Performance enhancements
- UI and accessibility improvements
- Roadmap features

### ❌ Please Avoid

- Large unrelated changes in a single pull request
- Unnecessary dependencies
- Major architectural refactors without discussion
- Breaking existing functionality

---

## 👨🏽‍💻 Development Notes

### Database Seeding

If you modify:

```text
counter/services/word_data.json
```

please run:

```bash
python -m counter.services.seed_origins
```

to verify the DuckDB database updates correctly.

### Environment

- Use a virtual environment.
- Manage dependencies through `pyproject.toml`.
- Update project dependencies when adding new packages.

### Code Style

- Follow PEP 8 guidelines.
- Prefer small, focused functions.
- Keep business logic inside the service layer where possible.
- Add comments where they improve readability or explain intent.

---

## 🧪 Testing

Before submitting a pull request, please ensure:

```bash
pytest
```

runs successfully.

Contributors are encouraged to add tests for:

- Analysis services
- Export functionality
- Database utilities
- Extraction pipelines
- New roadmap features

---

## 📸 UI Changes

If your contribution modifies the user interface, please include screenshots in your pull request.

---

## 🛣️ Roadmap Areas

Contributions are especially welcome in:

- Custom Stopword Management
- Analysis Tags & Collections
- Interactive Word Trends
- Enhanced Geospatial Mapping
- Readability Improvements
- Comparative Analysis Enhancements
- Reporting and Export Features

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 📬 Questions?
If you have any questions, feel free to open an issue or contact the maintainer at [reory35@hotmail.com].