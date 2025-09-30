from typing import List, Dict
import re


SAMPLE_JOBS: List[Dict] = [
    {
        "title": "Software Engineer - Backend",
        "company": "Acme Corp",
        "location": "Remote",
        "keywords": ["python", "flask", "api", "postgres", "docker"],
    },
    {
        "title": "Data Scientist",
        "company": "Insight Labs",
        "location": "New York, NY",
        "keywords": ["machine learning", "pandas", "scikit-learn", "nlp"],
    },
    {
        "title": "Frontend Engineer",
        "company": "Bright UI",
        "location": "San Francisco, CA",
        "keywords": ["react", "typescript", "css", "tailwind"],
    },
]


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_+\-#\.]+", text.lower())


def recommend_jobs(resume_text: str) -> List[Dict]:
    tokens = set(_tokenize(resume_text))
    scored = []
    for job in SAMPLE_JOBS:
        score = sum(1 for k in job["keywords"] if k.lower() in tokens)
        scored.append((score, job))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [job for score, job in scored if score > 0][:5]


