from core.ranker import CandidateRanker


def test_rank_score_range():
    ranker = CandidateRanker()
    score = ranker.rank(similarity=0.7, skill_count=8, project_count=3)

    assert 0.0 <= score <= 1.0
