from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class StructuredJDMatcher:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def match(self, resume, jd):
        resume_skills = set(map(str.lower, resume.skills))
        jd_skills = set(map(str.lower, jd.skills))

        if jd_skills:
            matched = resume_skills & jd_skills
            skill_score = len(matched) / len(jd_skills)
        else:
            skill_score = 1.0

        # Experience Match
        if jd.total_years_experience:
            if resume.total_years_experience:
                exp_score = min(
                    resume.total_years_experience / jd.total_years_experience,
                    1.0
                )
            else:
                exp_score = 0.0
        else:
            exp_score = 1.0


        # Role Match
        if resume.current_role and jd.current_role:
            r_vec = self.embedder.encode([resume.current_role])
            j_vec = self.embedder.encode([jd.current_role])
            role_score = cosine_similarity(r_vec, j_vec)[0][0]
        else:
            role_score = 0.5

        # Final Score
        final_score = (
            0.55 * skill_score +
            0.30 * exp_score +
            0.15 * role_score
        )

        return {
            "final_score": round(final_score, 3),
            "skill_score": round(skill_score, 3),
            "experience_score": round(exp_score, 3),
            "role_score": round(role_score, 3),
            "matched_skills": list(matched) if jd_skills else [],
            "missing_skills": list(jd_skills - resume_skills),
        }

