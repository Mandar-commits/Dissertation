from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from core.semantic_matcher import SemanticMatcher


class StructuredJDMatcher:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.semantic = SemanticMatcher()

    def match(self, resume, jd, resume_text=None, jd_text=None):
        resume_skills = set(map(str.lower, resume.skills))
        jd_skills = set(map(str.lower, jd.skills))

        matched = resume_skills & jd_skills
        missing = jd_skills - resume_skills

        skill_score = len(matched) / len(jd_skills) if jd_skills else 1

        # Expereience
        exp_score = 0
        if jd.total_years_experience and resume.total_years_experience:

            exp_score = min(
                resume.total_years_experience /
                jd.total_years_experience,
                1.0
            )

        # Semantic Similarity
        semantic_score = 0
        if resume_text and jd_text:
            semantic_score = self.semantic.compute(
                resume_text, jd_text
            )

        # Final Score
        final_score = (
            0.40 * skill_score +
            0.30 * exp_score +
            0.30 * semantic_score
        )

        return {
            "final_score": round(final_score, 3),

            "score_breakdown": {

                "skill_score": round(skill_score, 3),
                "experience_score": round(exp_score, 3),
                "semantic_score": round(semantic_score, 3),
            },

            "matched_skills": list(matched),
            "missing_skills": list(missing),

            "confidence": round(
                (skill_score + semantic_score)/2,
                3
            )
        }