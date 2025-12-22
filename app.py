from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from pypdf import PdfReader
from rapidfuzz import fuzz
import re

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        # pypdf returns None if no text; coerce to empty string
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text.strip()

# Lightweight similarity uses RapidFuzz; no heavyweight model needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}, 200

@app.route('/analyze', methods=['POST'])
def analyze():
    resume_file = request.files['resume']
    job_desc = request.form['job_description']

    if not resume_file or not job_desc:
        return "Resume file or job description missing.", 400

    filename = secure_filename(resume_file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume_file.save(save_path)

    resume_text = extract_text_from_pdf(save_path)

    # Similarity via token set ratio (0-100)
    match_score = float(fuzz.token_set_ratio(resume_text, job_desc))

    # Approximate "skills" by overlapping 4+ letter words between resume and JD
    resume_words = set(re.findall(r'\b\w{4,}\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b\w{4,}\b', job_desc.lower()))
    matched_skills = sorted(jd_words & resume_words)
    missing_skills = sorted(jd_words - resume_words)[:10]

    # Rule-based suggestions
    suggestions = []
    if "flask" in jd_words and "flask" not in resume_text.lower():
        suggestions.append("Mention your experience working with Flask or similar web frameworks.")
    if "sql" in jd_words and "sql" not in resume_text.lower():
        suggestions.append("Include your experience with SQL databases.")
    if "api" in jd_words and "api" not in resume_text.lower():
        suggestions.append("Describe any projects where you built or worked with APIs.")
    if len(resume_text.split()) < 150:
        suggestions.append("Your resume seems short. Add more details about your experience, skills, or projects.")
    if not any(heading in resume_text.lower() for heading in ["experience", "work", "project"]):
        suggestions.append("Consider adding an 'Experience' or 'Projects' section to highlight your background.")

    return render_template(
        'result.html',
        match_score=match_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        suggestions=suggestions
    )

if __name__ == '__main__':
    app.run(debug=True)
