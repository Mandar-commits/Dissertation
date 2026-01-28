import logging

logger = logging.getLogger(__name__)

class CandidateRanker:
    def rank(self, similarity: float, skill_count: int, project_count: int) -> float:
        logger.info("Ranking candidate")
        score = (0.6 * similarity) + (0.25 * min(skill_count / 10, 1)) + (0.15 * min(project_count / 5, 1))
        logger.debug(f"Final Ranking Score: {score}")
        return round(score, 3)