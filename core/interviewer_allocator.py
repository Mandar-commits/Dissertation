import logging

logger = logging.getLogger(__name__)

class InterviewerAllocator:
    """
    Assign interviewer based on:
    - skill overlap
    - experience band
    """
    def __init__(self):
        # Example interviewer skill profiles
        self.interviewers = [
            {
                "name": "Alice",
                "skills": {"python", "ml", "data", "ai"},
                "min_exp": 0,
                "max_exp": 3,
            },
            {
                "name":"Bob",
                "skills":{"backend", "java", "sql", "api"},
                "min_exp": 2,
                "max_exp": 6,
            },
            {
                "name": "Carol",
                "skills": {"cloud", "aws", "docker", "devops"},
                "min_exp": 3,
                "max_exp": 10,
            }
        ]

    def assign_one(self, resume):
        cand_skills = set(map(str.lower, resume.skills))
        cand_exp = resume.total_years_experience or 0

        best = None
        best_score = -1

        for iv in self.interviewers:
            skill_overlap = len(cand_skills & iv["skills"])

            exp_ok = iv["min_exp"] <= cand_exp <= iv["max_exp"]
            exp_score = 1 if exp_ok else 0

            score = skill_overlap * 2 + exp_score

            if score > best_score:
                best_score = score
                best = iv["name"]

        return best

    def assign_batch(self, resumes):
        result = {}
        for r in resumes:
            result[r.name or "Unknown"] = self.assign_one(r)
        return result
