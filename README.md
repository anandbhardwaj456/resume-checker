## Productivity & Work Tools – Flask App

This repository contains a Flask web app offering:

- AI Resume & Career Assistant
- Job Match recommender
- Smart Email Manager
- Meeting Assistant
- AI Document Search (TF-IDF)

### Quickstart

1. Create virtual environment
```bash
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app
```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

### Notes

- PDF and DOCX parsing require `pdfminer.six` and `python-docx`. If extraction fails, the app will gracefully degrade.
- Search uses TF-IDF cosine similarity over uploaded documents kept in-memory for the app lifetime.
- Do not use the development secret key in production. Set `SECRET_KEY` via environment variable and place uploads outside the repo in production.


