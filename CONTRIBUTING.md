# Contributing to Word Counter Vault

First off, thank you for considering contributing to the Word Counter Vault! It's people like you who make the open-source community such an amazing place to learn, inspire, and create.

## 📜 Code of Conduct
By participating in this project, you agree to maintain a professional and respectful environment for everyone.

## 🛠️ How Can I Contribute?

### Reporting Bugs
* Check the **Issues** tab to see if the bug has already been reported.
* If not, open a new issue. Clearly describe the problem, including steps to reproduce the bug and your operating system/browser details.

### Suggesting Enhancements
* Open an issue with the tag `enhancement`.
* Explain the "Why" behind the feature and how it would benefit users.

### Pull Requests (PRs)
1. **Fork** the repository.
2. **Create a branch** for your feature (`git checkout -b feature/AmazingFeature`).
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`).
4. **Push to the branch** (`git push origin feature/AmazingFeature`).
5. **Open a Pull Request**.

## 🏗️ Development Guidelines
* **Database Seeding:** If you modify `word_data.json`, you must run the seeding script (`python -m counter.services.seed_origins`) to verify the DuckDB file updates correctly.
* **Environment:** Ensure you are using a virtual environment and update `requirements.txt` if you add new dependencies.
* **Style:** Follow PEP 8 guidelines for Python code.

## 🧪 Testing
Before submitting a PR, please ensure:
1. The Django server starts without errors.
2. The DuckDB etymology lookup returns results for standard test words (e.g., "house", "logic", "banana").
3. PDF and Word exports generate correctly.

## 📬 Questions?
If you have any questions, feel free to open an issue or contact the maintainer at [reory35@hotmail.com].