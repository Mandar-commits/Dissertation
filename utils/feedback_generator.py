import logging

logger = logging.getLogger(__name__)

def generate_feedback(entities, similarity: float):
    logger.info("Generating JD-aware feedback")
    feedback = []

    if similarity < 0.5:
        feedback.append("Your Resume relevance to the job description is low.")

    if entities.total_years_experience and entities.total_years_experience < 2:
        feedback.append("Your Experience is below typical job requirements")

    if len(entities.skills) < 5:
        feedback.append("Consider adding more technical skills.")

    if not entities.projects:
        feedback.append("Add project experience to strengthen your profile.")

    return feedback