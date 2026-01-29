from core.structured_matcher import StructuredJDMatcher
from domain.entities import ResumeEntities

def pretty_print(result: dict):
    print("\n=== MATCH RESULT ===")
    print(f"Final Score        : {result['final_score']}")
    print(f"Skill Score        : {result['skill_score']}")
    print(f"Experience Score   : {result['experience_score']}")
    print(f"Role Score         : {result['role_score']}")
    print(f"Matched Skills     : {result['matched_skills']}")
    print(f"Missing Skills     : {result['missing_skills']}")
    print("====================\n")

if __name__ == "__main__":
    # Simulated JD Entities
    jd_entities = ResumeEntities(
        skills = ["Python", "SQL", "Docker", "AWS"],
        total_years_experience=3,
        current_role="Backend Engineer"
    )

    # Simulated Resume Entities
    resume_entities = ResumeEntities(
        name="John Doe",
        skills=["Python", "SQL", "Flask"],
        total_years_experience=2,
        current_role="Software Engineer"
    )

    matcher = StructuredJDMatcher()

    result = matcher.match(resume_entities, jd_entities)
    pretty_print(result)