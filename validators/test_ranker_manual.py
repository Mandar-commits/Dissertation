from core.ranker import CandidateRanker

if __name__ == "__main__":
    ranker = CandidateRanker()
    score = ranker.rank(similarity=0.72, skill_count=9, project_count=3)

    print("Rank Score")
    print(score)
