from utils.feedback_generator import generate_feedback
from domain.entities import ResumeEntities

if __name__ == "__main__":
    entities  = ResumeEntities(
        total_years_experience=1.2,
        skills=["Python"],
        projects=[],
    )

    feedback = generate_feedback(entities, "Skilled in Python, Required 3 years of experience", similarity=0.3)

    print("Feedback")
    for f in feedback:
        print("-", f)