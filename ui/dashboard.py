import streamlit as st
import time
import pandas as pd
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


# ---------------------------------------------------
# STREAMLIT PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Recruitment System",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Recruitment System")
st.caption("LLM-Powered Resume Extraction, Matching & Ranking")


# ---------------------------------------------------
# CACHE EXTRACTOR (CRITICAL FIX)
# ---------------------------------------------------

@st.cache_resource
def get_extractor():
    return UltraFastExtractor()

@st.cache_resource
def get_allocator():
    return InterviewerAllocator()

extractor = get_extractor()
allocator = get_allocator()


# ---------------------------------------------------
# PERFORMANCE TIMER
# ---------------------------------------------------

def timer():
    return time.time()


# ---------------------------------------------------
# SIDEBAR INFO
# ---------------------------------------------------

st.sidebar.header("System Info")

st.sidebar.success("LLM Model Loaded")
st.sidebar.info("Extractor Cached")
st.sidebar.info("Parallel Processing Enabled")


# ---------------------------------------------------
# JD SECTION
# ---------------------------------------------------

st.header("📄 Job Description Input")

jd_mode = st.radio(
    "Choose JD Input Mode",
    ["Manual Entry", "Upload JD File"],
    horizontal=True
)

if jd_mode == "Manual Entry":

    col1, col2 = st.columns(2)

    with col1:
        jd_skills = st.text_input(
            "Skills (comma separated)",
            placeholder="python, machine learning, sql"
        )

    with col2:
        jd_exp = st.number_input(
            "Minimum Experience (Years)",
            0.0, 30.0, 2.0
        )

    jd_role = st.text_input(
        "Role",
        placeholder="Data Scientist"
    )

    if st.button("Create JD", use_container_width=True):

        st.session_state.jd = ResumeEntities(
            skills=[s.strip().lower() for s in jd_skills.split(",") if s],
            total_years_experience=jd_exp,
            current_role=jd_role
        )

        st.success("JD Created")


else:

    jd_file = st.file_uploader(
        "Upload JD",
        type=["pdf", "docx"]
    )

    if jd_file and st.button("Extract JD", use_container_width=True):

        start = timer()

        text = ingest_resume(jd_file)
        jd_entity = extractor.extract(text)

        st.session_state.jd = jd_entity

        st.success(
            f"JD Extracted in {round(timer()-start,2)} sec"
        )


# Display JD

if "jd" in st.session_state:

    st.subheader("Extracted JD")

    st.json(st.session_state.jd.to_dict())


# ---------------------------------------------------
# RESUME SECTION
# ---------------------------------------------------

st.header("📂 Resume Upload")

files = st.file_uploader(
    "Upload resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


if files:

    if st.button("Extract Resumes", use_container_width=True):

        progress = st.progress(0)
        status = st.empty()

        start_time = timer()

        resumes = []

        total = len(files)

        for i, file in enumerate(files):

            status.text(f"Processing {file.name}")

            text = ingest_resume(file)

            entity = extractor.extract(text)

            resumes.append(entity)

            progress.progress((i+1)/total)

        st.session_state.resumes = resumes

        st.success(
            f"Extracted {total} resumes in {round(timer()-start_time,2)} sec"
        )


# ---------------------------------------------------
# RANKING SECTION
# ---------------------------------------------------

if "jd" in st.session_state and "resumes" in st.session_state:

    st.header("📊 Ranking")

    if st.button("Rank Candidates", use_container_width=True):

        with st.spinner("Matching resumes with JD..."):

            start = timer()

            ranked = rank_resume_against_jd(
                st.session_state.resumes,
                st.session_state.jd
            )

            st.session_state.ranked = ranked

            st.success(
                f"Ranking completed in {round(timer()-start,2)} sec"
            )


# ---------------------------------------------------
# RESULTS SECTION
# ---------------------------------------------------

if "ranked" in st.session_state:

    ranked = st.session_state.ranked

    st.header("🏆 Ranked Candidates")

    df = pd.DataFrame([
        {
            "Rank": r["rank"],
            "Name": r["name"],
            "Score": r["score"],
            "Experience": r["resume"]["total_years_experience"],
            "Skills": ", ".join(r["resume"]["skills"])
        }
        for r in ranked
    ])

    st.dataframe(df, use_container_width=True)


    # Detailed View

    st.subheader("Candidate Details")

    for r in ranked:

        with st.expander(f"Rank {r['rank']} — {r['name']}"):

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Final Score",
                    r["score"]
                )

                st.metric(
                    "Experience",
                    r["resume"]["total_years_experience"]
                )

            with col2:

                st.write("Matched Skills")
                st.success(
                    ", ".join(r["details"]["matched_skills"])
                )

                st.write("Missing Skills")
                st.error(
                    ", ".join(r["details"]["missing_skills"])
                )


# ---------------------------------------------------
# INTERVIEWER ASSIGNMENT
# ---------------------------------------------------

if "ranked" in st.session_state:

    st.header("👨‍💼 Interviewer Assignment")

    assignments = allocator.assign_batch(
        [ResumeEntities(**r["resume"]) for r in st.session_state.ranked]
    )

    st.json(assignments)


# ---------------------------------------------------
# DOWNLOAD RESULTS
# ---------------------------------------------------

if "ranked" in st.session_state:

    st.header("⬇ Download Results")

    export = pd.DataFrame(st.session_state.ranked)

    st.download_button(
        "Download Ranking CSV",
        export.to_csv(index=False),
        "ranking.csv",
        use_container_width=True
    )
