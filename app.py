import streamlit as st
import matplotlib.pyplot as plt
from utils import *
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
🚀 AI-Powered Resume Analyzer & ATS System
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Navigation")
option = st.sidebar.radio("Go to", ["Home", "About"])

# ---------------- ABOUT PAGE ----------------
if option == "About":
    st.title("📘 About This Project")

    st.write("""
🚀 **AI-Powered Smart Resume Analyzer & ATS System**

This project simulates a real-world ATS system used by companies.

It analyzes resumes using NLP techniques and compares them with job descriptions.

### 🔍 Features:
• ATS Score Calculation  
• Skill Matching  
• Missing Skills Detection  
• Resume Feedback  
• Job Role Prediction  
• Selection Probability  
• Data Visualization  

### 🛠 Tech Used:
Python, Streamlit, NLP, Scikit-learn, Matplotlib  

### 💡 Goal:
Help candidates improve resumes and increase job selection chances.
    """)
    st.stop()

# ---------------- FILE UPLOAD ----------------
st.subheader("📂 Upload Resume")
uploaded_file = st.file_uploader("Upload Resume (TXT or PDF)", type=["txt", "pdf"])

# ---------------- JOB DESCRIPTION ----------------
st.subheader("📝 Job Description")
job_description = st.text_area("Paste Job Description Here")

# ---------------- TEXT EXTRACTION ----------------
def extract_text(file):
    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text

    elif file.type == "text/plain":
        return file.read().decode("utf-8")

    return ""

# ---------------- ANALYZE BUTTON ----------------
if st.button("🚀 Analyze Resume"):

    if not uploaded_file:
        st.warning("⚠️ Please upload a resume")
        st.stop()

    if not job_description:
        st.warning("⚠️ Please enter job description")
        st.stop()

    resume_text = extract_text(uploaded_file)

    # ---------------- ATS SCORE ----------------
    ats_score, skill_score, keyword_score = calculate_ats_score(
        resume_text, job_description
    )

    st.markdown("## 📊 ATS Score Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📊 ATS Score", f"{ats_score}/100")

    with col2:
        st.metric("🎯 Skill Match", f"{round(skill_score,2)}%")

    with col3:
        st.metric("🔍 Keyword Match", f"{round(keyword_score,2)}%")

    st.progress(int(ats_score))

    st.markdown("---")

    # ---------------- SKILLS ----------------
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Your Skills")
        st.success(", ".join(resume_skills) if resume_skills else "No skills found")

    with col2:
        st.subheader("📋 Job Skills")
        st.info(", ".join(job_skills) if job_skills else "No skills found")

    st.markdown("---")

    # ---------------- MISSING SKILLS ----------------
    missing = missing_skills(resume_text, job_description)

    st.subheader("❌ Missing Skills")

    if len(missing) == 0:
        st.success("🎉 Perfect Match! No missing skills.")
    else:
        st.error(", ".join(missing))

    st.markdown("---")

    # ---------------- FEEDBACK ----------------
    feedback = get_feedback(resume_text, missing)

    st.subheader("📝 Suggestions")

    for tip in feedback:
        st.info(f"👉 {tip}")

    st.markdown("---")

    # ---------------- ROLE + PROBABILITY ----------------
    role = predict_role(resume_text)
    prob = selection_probability(ats_score)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Predicted Role")
        st.success(role)

    with col2:
        st.subheader("📌 Selection Chance")
        st.info(prob)

    st.markdown("---")

    # ---------------- VISUALIZATION ----------------
    st.subheader("📈 Score Breakdown")

    labels = ['Skills Match', 'Keyword Match']
    sizes = [skill_score, keyword_score]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.set_title("Match Distribution")

    st.pyplot(fig)

    st.markdown("---")

    # ---------------- SECTION ANALYSIS ----------------
    sections = section_analysis(resume_text)

    st.subheader("📊 Section Analysis")
    st.json(sections)

    st.markdown("---")

    # ---------------- RESUME STRENGTH ----------------
    st.subheader("💪 Resume Strength")

    if ats_score >= 80:
        st.success("🔥 Strong Resume")
    elif ats_score >= 60:
        st.warning("⚠️ Average Resume")
    else:
        st.error("❌ Needs Improvement")

    st.markdown("---")

    # ---------------- DOWNLOAD REPORT ----------------
    report = f"""
ATS Score: {ats_score}
Skills: {resume_skills}
Missing Skills: {missing}
Predicted Role: {role}
Selection Chance: {prob}
"""

    st.download_button("📥 Download Report", report, file_name="report.txt")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ by Gaurav Dwivedi | Final Year Project</center>",
    unsafe_allow_html=True
)
