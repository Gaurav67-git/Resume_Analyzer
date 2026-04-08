import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🔹 Extract Skills (basic list - you can expand)
SKILLS_DB = [
    "python", "java", "sql", "machine learning", "data analysis",
    "excel", "power bi", "tableau", "html", "css", "javascript",
    "react", "node", "nlp", "deep learning"
]

# 🔹 Extract text features
def extract_skills(text):
    text = text.lower()
    found_skills = [skill for skill in SKILLS_DB if skill in text]
    return list(set(found_skills))

# 🔹 Keyword matching using TF-IDF
def keyword_match(resume, job_desc):
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume, job_desc])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return score * 100

# 🔹 ATS Score (Weighted)
def calculate_ats_score(resume, job_desc):
    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job_desc)

    if len(job_skills) == 0:
        skill_score = 0
    else:
        matched = len(set(resume_skills) & set(job_skills))
        skill_score = (matched / len(job_skills)) * 100

    keyword_score = keyword_match(resume, job_desc)

    # Simple experience check
    experience_score = 70 if "experience" in resume.lower() else 30

    # Formatting check
    format_score = 80 if len(resume) > 300 else 50

    final_score = (
        0.4 * skill_score +
        0.25 * experience_score +
        0.2 * keyword_score +
        0.15 * format_score
    )

    return round(final_score, 2), skill_score, keyword_score

# 🔹 Missing Skills
def missing_skills(resume, job_desc):
    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job_desc)
    return list(set(job_skills) - set(resume_skills))

# 🔹 Feedback Generator
def get_feedback(resume, missing):
    feedback = []

    if len(missing) > 0:
        feedback.append(f"Add missing skills: {', '.join(missing)}")

    if "project" not in resume.lower():
        feedback.append("Add project section")

    if "achievement" not in resume.lower():
        feedback.append("Include achievements with numbers")

    if len(resume.split()) < 150:
        feedback.append("Resume content is too short")

    if "python" not in resume.lower():
        feedback.append("Add technical skills like Python")

    return feedback

# 🔹 Job Role Prediction
def predict_role(resume):
    resume = resume.lower()

    if "machine learning" in resume or "nlp" in resume:
        return "Machine Learning Engineer"
    elif "sql" in resume or "data analysis" in resume:
        return "Data Analyst"
    elif "react" in resume or "javascript" in resume:
        return "Web Developer"
    else:
        return "General Software Role"


def selection_probability(ats_score):
     if ats_score >= 80:
        return "High (80-95%)"
     elif ats_score >= 60:
        return "Medium (50-75%)"
     else:
        return "Low (20-50%)"

def section_analysis(resume):
    score = {}

    score['Skills Section'] = 80 if "skills" in resume.lower() else 40
    score['Projects Section'] = 80 if "project" in resume.lower() else 40
    score['Experience Section'] = 80 if "experience" in resume.lower() else 40

    return score