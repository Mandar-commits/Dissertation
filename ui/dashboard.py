import streamlit as st

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.logging_config import setup_logging
setup_logging()

from core.ingestion import ingest_resume
from core.llm_extractor import LLMEntityExtractor
from core.section_pipeline import process_resume
from core.matcher import ResumeJDMatcher
from core.ranker import CandidateRanker
from core.interviewer_allocator import InterviewerAllocator
from utils.feedback_generator import generate_feedback
from utils.exporter import export_json, export_csv

st.set_page_config(page_title="AI Recruitment System", layout="wide")

st.title("AI Recruitment System (Local LLM)")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Resume Upload", "JD Upload", "Results", "Admin Debug"]
)

resume_text = None
jd_text = None
entities = None
similarity = None
rank_score = None
feedback = None
assignments = None

# Resume Upload
with tab1:
    st.subheader("Upload Resume (PDF/DOC)")
    resume_file = st.file_uploader(
        "Upload Resume", type=["pdf", "docx"], key="resume"
    )

    if resume_file:
        with st.spinner("Extracting resume text... "):
            resume_text = ingest_resume(resume_file)
        st.success("Resume text extracted successfully")
        st.text_area("Resume Text (Preview)", resume_text[:3000], height=250)


# Job Description Upload
with tab2:
    st.subheader("Upload Job Description (PDF/DOCX)")
    jd_file = st.file_uploader(
        "Upload Job Description", type=["pdf", "docx"], key="jd"
    )

    if jd_file:
        with st.spinner("Extracting JD text"):
            jd_text = ingest_resume(jd_file)
        st.success("Job Description text extracted successfully")
        st.text_area("JD Text (Preview)", jd_text[:3000], height=250)

# Pipeline Execution
if resume_text and jd_text:
    extractor = LLMEntityExtractor()
    matcher = ResumeJDMatcher()
    ranker = CandidateRanker()
    allocator = InterviewerAllocator()

    with st.spinner("Running AI recruitment pipeline..."):
        entities = process_resume(extractor.extract(resume_text))
        similarity = matcher.compute_similarity(resume_text, jd_text)
        rank_score = ranker.rank(
            similarity, len(entities.skills), len(entities.projects)
        )
        feedback = generate_feedback(entities, similarity)

        result = {
            "name": entities.name,
            "email": entities.email,
            "phone": entities.phone,
            "current_role": entities.current_role,
            "total_years_experience": entities.total_years_experience,
            "skills": entities.skills,
            "education": entities.education,
            "experience": entities.experience,
            "projects": entities.projects,
            "certifications": entities.certifications,
            "similarity": similarity,
            "rank_score": rank_score
        }

        interviewers = ["Alice", "Bob", "Carol"]
        assignments = allocator.assign([result], interviewers)

# Results
with tab3:
    if entities:
        st.subheader("Resume-JD Similarity")
        st.metric("Similarity Score", round(similarity,3))

        st.subheader("Final Candidate Rank")
        st.metric("Rank Score", rank_score)

        st.subheader("Extracted Resume Entities")
        st.json(entities.to_dict())

        st.subheader("Interviewer Assignment")
        st.json(assignments)

        st.subheader("JD-Aware Feedback")
        for f in feedback:
            st.write(".", f)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Export Result as JSON"):
                export_json(result)
                st.success("Exported to outputs/results.json")

        with col2:
            if st.button("Export Result as CSV"):
                export_csv(result)
                st.success("Exported to outputs/results.csv")

    else:
        st.info("Upload both Resume and Job Description to see results")


# Admin Debug Panel
with tab4:
    st.subheader("Debug Panel")

    if resume_text:
        st.text_area("Full Resume Text", resume_text, height=250)

    if jd_text:
        st.text_area("Full JD Text", jd_text, height=250)

    if entities:
        st.subheader("Raw Entity JSON")
        st.json(entities.to_dict())

    if similarity is not None:
        st.write("Similarity:", similarity)

    if rank_score is not None:
        st.write("Rank Score:", rank_score)

    if feedback:
        st.write("Feedback", feedback)

    if assignments:
        st.write("Assignments:", assignments)
