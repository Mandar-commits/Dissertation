from domain.entities import ResumeEntities


def test_entities_creation():
    e = ResumeEntities(
        name="John Doe",
        email="john@example.com",
        phone="1234567890",
        current_role="ML Engineer",
        total_years_experience=3.5,
        skills=["Python", "SQL"],
        projects=["ATS System"],
    )

    assert e.name == "John Doe"
    assert e.email == "john@example.com"
    assert e.total_years_experience == 3.5
    assert "Python" in e.skills
