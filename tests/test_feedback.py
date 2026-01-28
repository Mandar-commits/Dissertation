from utils.feedback_generator import generate_feedback
from domain.entities import ResumeEntities


def test_feedback_low_profile():
    entities = ResumeEntities(
        total_years_experience=1,
        skills=["Python"],
        projects=[],
    )

    feedback = generate_feedback(entities, similarity=0.3)

    assert len(feedback) >= 2
    assert any("relevance" in f.lower() or "experience" in f.lower() for f in feedback)
