from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from services.resume import parse_resume_file, suggest_resume_improvements, generate_cover_letter
from services.jobs import recommend_jobs
from services.email_manager import categorize_email, prioritize_score, summarize_email, draft_email_reply
from services.meeting import summarize_transcript, extract_action_items
from services.search_engine import DocumentSearchIndex


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_DOC_EXTENSIONS = {"txt", "pdf", "docx"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_DOC_EXTENSIONS


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"  # replace in production
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Shared in-memory index for the app lifetime
search_index = DocumentSearchIndex()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resume", methods=["GET", "POST"])
def resume_assistant():
    parsed_text = None
    suggestions = []
    cover_letter = None

    if request.method == "POST":
        if "resume" not in request.files:
            flash("No file part in request", "error")
            return redirect(request.url)
        file = request.files["resume"]
        if file.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)

            parsed_text = parse_resume_file(save_path)
            suggestions = suggest_resume_improvements(parsed_text)

            job_desc = request.form.get("job_description", "").strip()
            if job_desc:
                cover_letter = generate_cover_letter(parsed_text, job_desc)
        else:
            flash("Unsupported file type. Allowed: txt, pdf, docx", "error")

    return render_template(
        "resume.html",
        parsed_text=parsed_text,
        suggestions=suggestions,
        cover_letter=cover_letter,
    )


@app.route("/jobs", methods=["GET", "POST"])
def job_match():
    recommendations = []
    resume_text = ""
    if request.method == "POST":
        resume_text = request.form.get("resume_text", "").strip()
        if resume_text:
            recommendations = recommend_jobs(resume_text)
        else:
            flash("Please paste resume text for job recommendations.", "error")
    return render_template("jobs.html", recommendations=recommendations, resume_text=resume_text)


@app.route("/email", methods=["GET", "POST"])
def email_manager():
    email_text = ""
    category = None
    priority = None
    summary = None
    reply = None
    if request.method == "POST":
        email_text = request.form.get("email_text", "").strip()
        if email_text:
            category = categorize_email(email_text)
            priority = prioritize_score(email_text)
            summary = summarize_email(email_text)
            tone = request.form.get("tone", "professional")
            reply = draft_email_reply(email_text, tone)
        else:
            flash("Please paste an email to analyze.", "error")
    return render_template(
        "email.html",
        email_text=email_text,
        category=category,
        priority=priority,
        summary=summary,
        reply=reply,
    )


@app.route("/meeting", methods=["GET", "POST"])
def meeting_assistant():
    transcript = ""
    summary = None
    action_items = []
    if request.method == "POST":
        transcript = request.form.get("transcript", "").strip()
        if transcript:
            summary = summarize_transcript(transcript)
            action_items = extract_action_items(transcript)
        else:
            flash("Please paste a transcript to process.", "error")
    return render_template("meeting.html", transcript=transcript, summary=summary, action_items=action_items)


@app.route("/search", methods=["GET", "POST"])
def document_search():
    results = []
    query = ""
    if request.method == "POST":
        if "document" in request.files and request.files["document"].filename:
            file = request.files["document"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(save_path)
                # Index it
                search_index.add_document_from_path(save_path)
            else:
                flash("Unsupported file type for upload.", "error")

        query = request.form.get("query", "").strip()
        if query:
            results = search_index.search(query, top_k=5)

    indexed_docs_count = search_index.num_documents()
    return render_template("search.html", results=results, query=query, indexed_docs_count=indexed_docs_count)


if __name__ == "__main__":
    app.run(debug=True)


