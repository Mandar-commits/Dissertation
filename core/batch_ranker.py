from core.structured_matcher import StructuredJDMatcher
from core.ranker import CandidateRanker

def rank_resume_against_jd(resumes, jd_entities):
    matcher = StructuredJDMatcher()
    ranker = CandidateRanker()

    results = []

    for idx, resume in enumerate(resumes):
        match = matcher.match(resume, jd_entities)

        results.append({
            "resume_id": idx,
            "name": resume.name,
            "score": match["final_score"],
            "details": match,
            "resume": resume.to_dict(),
        })

    return ranker.rank_batch(results)