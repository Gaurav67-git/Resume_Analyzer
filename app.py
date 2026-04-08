import streamlit as st
import matplotlib.pyplot as plt
from utils import *
import PyPDF2
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Navigation")
option = st.sidebar.radio("Go to", ["Home", "About"])

# 🔥 IMPORTANT: Dark Mode Toggle (FIXED)
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

# ---------------- FULL DARK MODE ----------------
if dark_mode:
    st.markdown("""
    <style>

    /* ===== BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #020617, #0B1220);
    }

    .block-container {
        background: transparent;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1E293B;
    }

    /* ===== TEXT ===== */
    * {
        color: #E2E8F0 !important;
    }

    /* ===== FILE UPLOADER FULL FIX 🔥 ===== */
    div[data-testid="stFileUploader"] {
        background: linear-gradient(145deg, #1E293B, #0F172A);
        border-radius: 14px;
        border: 1px solid #334155;
        padding: 15px;
    }

    /* REMOVE WHITE INNER BOX */
    div[data-testid="stFileUploader"] section {
        background: transparent !important;
    }

    /* FIX BROWSE BUTTON 🔥 */
    div[data-testid="stFileUploader"] button {
        background: #2563EB !important;
        color: white !important;
        border-radius: 8px;
        border: none;
    }

    div[data-testid="stFileUploader"] button:hover {
        background: #1D4ED8 !important;
    }

    /* ===== TEXT AREA ===== */
    textarea {
        background-color: #1E293B !important;
        border: 1px solid #334155;
        border-radius: 12px;
        color: #E2E8F0 !important;
    }

    /* ===== BUTTON ===== */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB, #3B82F6);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
    }

    .stButton > button:hover {
        box-shadow: 0px 0px 15px #2563EB;
        transform: scale(1.03);
        transition: 0.3s;
    }

    /* ===== METRIC CARDS ===== */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1E293B, #0F172A);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #334155;
    }

    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #2563EB, #60A5FA);
    }
    
    /* 🔥 FIX DOWNLOAD BUTTON VISIBILITY */
.stDownloadButton > button {
    background: linear-gradient(135deg, #22C55E, #16A34A) !important;
    color: white !important;
    border-radius: 10px;
    border: none;
    padding: 10px 18px;
    font-weight: 600;
}

/* Hover effect */
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #16A34A, #15803D) !important;
    box-shadow: 0px 0px 12px #22C55E;
    transform: scale(1.03);
    transition: 0.3s;
}

    </style>
    """, unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI Resume Analyzer & ATS System</h1>
<p style='text-align:center;'>Analyze your resume like a real ATS system</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- ABOUT ----------------
if option == "About":

    st.markdown("## 📘 About This Project")

    # 🔥 Dynamic colors based on theme
    if dark_mode:
        bg = "linear-gradient(145deg, #1E293B, #0F172A)"
        text = "#E2E8F0"
        border = "#334155"
    else:
        bg = "linear-gradient(145deg, #FFFFFF, #F1F5F9)"
        text = "#1E293B"
        border = "#CBD5F5"

    st.markdown(f"""
    <div style="padding:25px; border-radius:15px;
                background:{bg};
                border:1px solid {border};
                color:{text};">

    <h3>🚀 AI-Powered Smart Resume Analyzer & ATS System</h3>

    <p>
    This project is a modern AI-based web application that simulates how real-world Applicant Tracking Systems (ATS) work in recruitment.
    </p>

    <p>
    It analyzes resumes using <b>NLP and machine learning</b> techniques and evaluates:
    <b>skills matching, keyword relevance, resume structure, and content quality</b>.
    </p>

    <hr>

    <h4>🔍 Key Features</h4>
    <ul>
        <li>📄 Supports TXT & PDF resumes</li>
        <li>🎯 Intelligent ATS scoring</li>
        <li>🧠 Skill extraction & matching</li>
        <li>❌ Missing skills detection</li>
        <li>📝 Smart suggestions</li>
        <li>🎯 Job role prediction</li>
        <li>📊 Dashboard & visualization</li>
        <li>📌 Selection probability</li>
    </ul>

    <hr>

    <h4>💡 Objective</h4>
    <p>
    Help candidates improve resumes and increase chances of selection.
    </p>

    <hr>

    <h4>🛠 Technologies</h4>
    <p>
    Python, Streamlit, Scikit-learn, NLP, PyPDF2, Matplotlib
    </p>

    </div>
    """, unsafe_allow_html=True)


    st.stop()
# ---------------- INPUT SECTION ----------------
st.subheader("📂 Upload Resume")
uploaded_file = st.file_uploader("Upload Resume (TXT/PDF)", type=["txt", "pdf"])

st.subheader("📝 Job Description")
job_description = st.text_area("Paste Job Description")

# ---------------- TEXT EXTRACTION ----------------
def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    return ""

def generate_pdf(report_text):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    # ---------------- TITLE ----------------
    title = Paragraph(
        "<b><font size=18 color='blue'>AI Resume Analysis Report</font></b>",
        styles["Title"]
    )
    content.append(title)
    content.append(Spacer(1, 15))

    # ---------------- SUBTITLE ----------------
    subtitle = Paragraph(
        "<font size=10 color='grey'>Generated by AI Resume Analyzer</font>",
        styles["Normal"]
    )
    content.append(subtitle)
    content.append(Spacer(1, 20))

    # ---------------- BODY ----------------
    for line in report_text.strip().split("\n"):

        line = line.strip()

        if not line:
            content.append(Spacer(1, 10))
            continue

        # Section headings
        if "ATS Score" in line or "Skill Match" in line or "Keyword Match" in line:
            content.append(Paragraph(f"<b>{line}</b>", styles["Heading3"]))

        elif "Your Skills" in line or "Job Required Skills" in line \
             or "Missing Skills" in line or "Predicted Role" in line \
             or "Selection Probability" in line or "Suggestions" in line:
            content.append(Paragraph(f"<b>{line}</b>", styles["Heading2"]))

        else:
            content.append(Paragraph(line, styles["Normal"]))

        content.append(Spacer(1, 8))

    # ---------------- FOOTER ----------------
    content.append(Spacer(1, 20))
    footer = Paragraph(
        "<font size=9 color='grey'>© AI Resume Analyzer Report</font>",
        styles["Normal"]
    )
    content.append(footer)

    doc.build(content)
    buffer.seek(0)

    return buffer

if "download_clicked" not in st.session_state:
    st.session_state.download_clicked = False

# ---------------- ANALYZE ----------------
if st.button("🚀 Analyze Resume"):

    if not uploaded_file:
        st.warning("⚠️ Upload resume")
        st.stop()

    if not job_description:
        st.warning("⚠️ Enter job description")
        st.stop()

    resume_text = extract_text(uploaded_file)

    ats_score, skill_score, keyword_score = calculate_ats_score(
        resume_text, job_description
    )

    # ---------------- DASHBOARD ----------------
    st.subheader("📊 ATS Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("ATS Score", f"{ats_score}/100")
    col2.metric("Skill Match", f"{round(skill_score,2)}%")
    col3.metric("Keyword Match", f"{round(keyword_score,2)}%")

    st.progress(int(ats_score))
    st.markdown("---")

    # ---------------- SKILLS ----------------
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Your Skills")
        st.success(", ".join(resume_skills) or "No skills found")

    with col2:
        st.subheader("📋 Job Skills")
        st.info(", ".join(job_skills) or "No skills found")

    st.markdown("---")

    # ---------------- MISSING ----------------
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

    # ---------------- ROLE ----------------
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

    # ---------------- CHART ----------------
    st.subheader("📈 Analysis")

    fig, ax = plt.subplots()
    ax.pie([skill_score, keyword_score],
           labels=["Skills", "Keywords"],
           autopct="%1.1f%%")

    st.pyplot(fig)

    # ---------------- PDF REPORT ----------------
    report = f"""
    AI RESUME ANALYSIS REPORT

    ATS Score: {ats_score}/100
    Skill Match: {round(skill_score,2)}%
    Keyword Match: {round(keyword_score,2)}%

    Your Skills:
    {", ".join(resume_skills)}

    Job Required Skills:
    {", ".join(job_skills)}

    Missing Skills:
    {", ".join(missing) if missing else "None - Perfect Match"}

    Predicted Role:
    {role}

    Selection Probability:
    {prob}

    Suggestions:
    {chr(10).join(['- ' + tip for tip in feedback])}
    """

    pdf_file = generate_pdf(report)

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_file,
        file_name="Resume_Report.pdf",
        mime="application/pdf"
    )
# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<center>✨ Resume Analyzer @2026 | Made by Team Alpha</center>
""", unsafe_allow_html=True)
