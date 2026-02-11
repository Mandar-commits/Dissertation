import streamlit as st

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.logging_config import setup_logging
setup_logging()

from domain.entities import ResumeEntities
from core.ingestion import ingest_resume
from core.fast_extractor import UltraFastExtractor
from core.batch_ranker import rank_resume_against_jd
from core.interviewer_allocator import InterviewerAllocator
from core.parallel_extract import extract_resumes_parallel

st.set_page_config(page_title="AI Recruitment System")
st.title("AI Recruitment System - Batch Resume Ranking (JD-Aware)")

extractor = UltraFastExtractor()
allocator = InterviewerAllocator()

# JD Input Manual or File

st.header("Job Description Input")

jd_mode = st.radio(
    "JD Input Mode",
    ["Manual Entry", "Upload JD File"]
)

jd_entities  = None

if jd_mode == "Manual Entry":
    jd_skills = st.text_input("JD Skills (Comma Separated)")
    jd_exp = st.number_input("Minimum Years Experience", 1.0, 30.0, 2.0)

    if st.button("Create JD"):
        jd_entities = ResumeEntities(
            skills=[s.strip().lower() for s in jd_skills.split(",") if s.strip()],
            total_years_experience=jd_exp,
            current_role="manual_jd"
        )
        st.session_state.jd = jd_entities
        st.success("JD Created")
else:
    jd_file = st.file_uploader("Upload JD PDF/DOCX", type=["pdf", "docx"])

    if jd_file and st.button("Extract JD"):
        text = ingest_resume(jd_file)
        jd_entities = extractor.extract(text)
        st.session_state.jd = jd_entities
        st.success("JD extracted")

if "jd" in st.session_state:
    st.json(st.session_state.jd.to_dict())

# Resume Input - Manual or Files

st.header("Resume Input")

resume_mode = st.radio(
    "Resume Mode",
    ["Manual Entry", "Upload Resume Files"]
)

resumes = []

if resume_mode == "Manual Entry":

    count = st.number_input("Number of Candidates", 1, 20, 1)

    manual_resumes = []

    for i in range(count):
        st.subheader(f"Candidate {i+1}")

        name = st.text_input(f"Name{i}", key=f"name{i}")
        skills = st.text_input(f"Skills {i} (comma separated)", key=f"skills{i}")
        exp = st.number_input(f"Experience {i}", 0.0, 30.0, 1.0, key=f"exp{i}")

        manual_resumes.append(
            ResumeEntities(
                name=name,
                skills=[s.strip().lower() for s in skills.split(",") if s.strip()],
                total_years_experience=exp
            )
        )

    if st.button("Load Manual Candidates"):
        st.session_state.resumes = manual_resumes
        st.success("Manual candidates loaded")

else:
    files = st.file_uploader(
        "Upload Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if files and st.button("Extract Resumes"):
        extracted = []
        for f in files:
            text = ingest_resume(f)
            extracted.append(extractor.extract(text))

        st.session_state.resumes = extracted
        st.success("Resumes extracted")

# Ranking Button

st.header("Ranking")

if "jd" in st.session_state and "resumes" in st.session_state:

    if st.button("Rank All Candidates"):

        ranked = rank_resume_against_jd(
            st.session_state.resumes,
            st.session_state.jd
        )

        st.session_state.ranked = ranked


# Results

if "ranked" in st.session_state:
    st.header("Ranked Results")
    ranked = st.session_state.ranked

    for r in ranked:
        st.write(
            f"**Rank {r['rank']} - {r['name']} - Score {r['score']}**"
        )

        st.write("Matched: ", r["details"]["matched_skills"])
        st.write("Missing: ", r["details"]["missing_skills"])
        st.divider()

    # Interviewer Assignment
    st.header("Interviewer Assignment")

    assignments = allocator.assign_batch(
        [ResumeEntities(**r["resume"]) for r in ranked]
    )

    st.json(assignments)