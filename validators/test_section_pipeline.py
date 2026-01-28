from core.section_pipeline import process_resume
from domain.entities import ResumeEntities

if __name__ == "__main__":
    entities = ResumeEntities(
        skills = ["Python", "python", "SQL"],
        education = ["BSc", "CS", "BSc", "CS"],
        projects = ["ATS", "ATS"]
    )

    cleaned = process_resume(entities)
    print(" Cleaned Entites ")
    print(cleaned.to_dict())