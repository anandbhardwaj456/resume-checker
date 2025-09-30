import os
from typing import List

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
        return ""  # gracefully degrade
    return extract_pdf_text(path) or ""


def _read_docx(path: str) -> str:
    if docx is None:
        return ""
    document = docx.Document(path)
    return "\n".join(p.text for p in document.paragraphs)


def parse_resume_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        return _read_txt(path)
    if ext == ".pdf":
        return _read_pdf(path)
    if ext == ".docx":
        return _read_docx(path)
    return ""


def suggest_resume_improvements(text: str) -> List[str]:
    if not text:
        return [
            "Could not parse resume content. Provide a .txt, .pdf, or .docx file.",
        ]
    suggestions: List[str] = []

    if len(text) < 800:
        suggestions.append("Expand content with measurable achievements and impact.")
    if "summary" not in text.lower() and "objective" not in text.lower():
        suggestions.append("Add a brief professional summary at the top.")
    if "%" not in text and any(k in text.lower() for k in ["improved", "increased", "reduced"]):
        suggestions.append("Quantify results with metrics (%, revenue, users, time saved).")
    if "experience" not in text.lower():
        suggestions.append("Add a dedicated Experience section with responsibilities and results.")
    if "skills" not in text.lower():
        suggestions.append("Include a Skills section with relevant tools and technologies.")
    if "education" not in text.lower():
        suggestions.append("Include an Education section with degree, institution, and year.")

    if not suggestions:
        suggestions.append("Your resume has strong structure. Consider tailoring keywords per job.")
    return suggestions


def generate_cover_letter(resume_text: str, job_description: str) -> str:
    intro = (
        "Dear Hiring Manager,\n\n"
        "I am excited to apply for the role at your organization. My background aligns "
        "well with your needs, and I bring a track record of delivering results.\n\n"
    )
    body = (
        "From my experience highlighted in my resume, I have demonstrated ownership, collaboration, "
        "and an ability to translate goals into measurable outcomes. In reviewing your job description, "
        "I believe my skills match the core requirements.\n\n"
    )
    tailoring = f"Relevant alignment to the role: {job_description[:600]}\n\n" if job_description else ""
    closing = (
        "I would welcome the opportunity to discuss how I can contribute.\n\n"
        "Sincerely,\nYour Name"
    )
    return intro + body + tailoring + closing


