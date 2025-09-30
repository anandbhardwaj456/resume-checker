import os
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from pdfminer.high_level import extract_text as extract_pdf_text
except Exception:  # pragma: no cover - optional dep
    extract_pdf_text = None

try:
    import docx  # python-docx
except Exception:  # pragma: no cover - optional dep
    docx = None


def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _read_pdf(path: str) -> str:
    if extract_pdf_text is None:
        return ""
    return extract_pdf_text(path) or ""


def _read_docx(path: str) -> str:
    if docx is None:
        return ""
    document = docx.Document(path)
    return "\n".join(p.text for p in document.paragraphs)


def read_any(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        return _read_txt(path)
    if ext == ".pdf":
        return _read_pdf(path)
    if ext == ".docx":
        return _read_docx(path)
    return ""


class DocumentSearchIndex:
    def __init__(self) -> None:
        self.paths: List[str] = []
        self.docs: List[str] = []
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = None

    def add_document_from_path(self, path: str) -> None:
        text = read_any(path)
        if not text:
            return
        self.paths.append(path)
        self.docs.append(text)
        self._rebuild()

    def _rebuild(self) -> None:
        if not self.docs:
            self.matrix = None
            return
        self.matrix = self.vectorizer.fit_transform(self.docs)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float, str]]:
        if not self.docs:
            return []
        if self.matrix is None:
            self._rebuild()
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.matrix)[0]
        ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:top_k]
        results: List[Tuple[str, float, str]] = []
        for idx, score in ranked:
            snippet = self.docs[idx][:300].replace("\n", " ")
            results.append((self.paths[idx], float(score), snippet))
        return results

    def num_documents(self) -> int:
        return len(self.docs)


