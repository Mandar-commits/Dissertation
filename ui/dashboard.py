import streamlit as st

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.logging_config import setup_logging
setup_logging()

from core.ingestion import ingest_resume
from core.llm_extractor import LLMEntityExtractor
from core.batch_ranker import rank_resume_against_jd
from utils.exporter import export_json, export_csv

st.set_page_config(page_title="AI Recruitment System")
st.title("AI Recruitment System - Batch Resume Ranking (JD-Aware)")

# State
if "ranked_results" not in st.session_state:
    st.session_state.ranked_results = None

# JD Upload
st.header("Upload Job Description")

jd_file = st.file_uploader(
    "Upload Job Description (PDF/DOCX)",
    type=["pdf", "docx"],
    key="JD"
)

jd_entities = None
extractor = LLMEntityExtractor()

if jd_file:
    with st.spinner("Extracting JD...."):
        jd_text = ingest_resume(jd_file)
        jd_entities = extractor.extract(jd_text)

    st.success("Job Description processed successfully")
    st.json(jd_entities.to_dict())


# Resume Upload Multiple Files
st.header("Upload Resumes")

resume_files = st.file_uploader(
    "Upload one or more resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    key="Resumes"
)


# Run Pipeline
if jd_entities and resume_files:
    if st.button("Rank Candidates"):
        resumes = []

        with st.spinner("Extracting Resumes....."):
            for file in resume_files:
                text = ingest_resume(file)
                entities = extractor.extract(text)
                resumes.append(entities)

        with st.spinner("matching & Ranking Candidates...."):
            ranked_results = rank_resume_against_jd(resumes, jd_entities)
            st.session_state.ranked_results = ranked_results


# Results
if st.session_state.ranked_results:
    st.header("Ranked Candidates")

    ranked = st.session_state.ranked_results

    # Summary Table
    table_data = []
    for r in ranked:
        table_data.append({
            "Rank": r["rank"],
            "Name": r["name"],
            "Score": r["score"],
            "Matched Skills": ", ".join(r["details"]["matched_skills"]),
            "Missing Skills": ", ".join(r["details"]["missing_skills"]),
        })

st.dataframe(table_data, use_container_width=True)


# Detailed View
st.subheader("Candidate Details")

for r in ranked:
    with st.expander(f"#{r['rank']} - {r['name']} (Score: {r['score']}"):
        st.json(r)

# Export
st.header("Export Results")

col1, col2 = st.columns(2)

with col1:
    if st.button("Export JSON"):
        export_json(ranked, "outputs/batch_results.json")
        st.success("Exported to outputs/batch_results.json")

with col2:
    if st.button("Export CSV"):
        export_csv(
            {r["name"]: r["score"] for r in ranked},
            "outputs/batch_results.csv"
        )
        st.success("Exported to outputs/batch_results.csv")