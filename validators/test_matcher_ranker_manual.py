"""
Validator for Resume-JD Matcher and Ranker

Steps:
1. Load resume PDF
2. Extract entities using UltraFastExtractor
3. Create JD entities manually
4. Run matcher
5. Rank candidates
6. Show explainable output
"""

import os
import time
from pathlib import Path

from core.fast_extractor import UltraFastExtractor
from core.batch_ranker import rank_resume_against_jd
from domain.entities import ResumeEntities

# PDF loader (use your existing loader if different)


# ============================
# CONFIG
# ============================

RESUME_FOLDER = ""

# Manual JD definition
JD_SKILLS = [
    "python",
    "machine learning",
    "deep learning",
    "django",
    "tensorflow",
    "sql"
]

JD_ROLE = "Data Scientist"

JD_EXPERIENCE = 2.0


# ============================
# PDF TEXT LOADER
# ============================



# ============================
# CREATE JD ENTITY
# ============================

def create_jd_entity():

    jd = ResumeEntities(
        name="JOB_DESCRIPTION",
        skills=JD_SKILLS,
        current_role=JD_ROLE,
        total_years_experience=JD_EXPERIENCE,
        education=[],
        projects=[]
    )

    return jd


# ============================
# MAIN VALIDATOR
# ============================

def run_validator():

    print("\n=========== MATCHER VALIDATOR ===========\n")

    extractor = UltraFastExtractor()

    jd_entity = create_jd_entity()

    resumes = []

    resume_texts = []

    folder = Path(RESUME_FOLDER)

    start_time = time.time()

    for file in folder.glob("*.pdf"):

        print(f"\nProcessing: {file.name}")

        text = load_pdf_text(file)

        entities = extractor.extract(text)

        resumes.append(entities)

        resume_texts.append(text)


    print("\nRunning Matcher + Ranker...\n")

    ranked = rank_resume_against_jd(
        resumes,
        jd_entity
    )

    total_time = time.time() - start_time


    # ============================
    # DISPLAY RESULTS
    # ============================

    print("\n=========== FINAL RANKING ===========\n")

    for candidate in ranked:

        print(f"Rank: {candidate['rank']}")
        print(f"Name: {candidate['name']}")
        print(f"Score: {candidate['score']}")

        details = candidate["details"]

        print("\nScore Breakdown:")
        print(f"  Skill Score: {details['score_breakdown']['skill_score']}")
        print(f"  Experience Score: {details['score_breakdown']['experience_score']}")
        print(f"  Role Score: {details['score_breakdown']['role_score']}")
        print(f"  Semantic Score: {details['score_breakdown']['semantic_score']}")

        print("\nMatched Skills:")
        print(details["matched_skills"])

        print("\nMissing Skills:")
        print(details["missing_skills"])

        print("\nConfidence:", details["confidence"])

        print("\n------------------------------------\n")


    print("Total Processing Time:", round(total_time, 2), "sec")


# ============================
# ENTRY POINT
# ============================

if __name__ == "__main__":

    run_validator()
