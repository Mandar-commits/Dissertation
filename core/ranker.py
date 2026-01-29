import logging

logger = logging.getLogger(__name__)

class CandidateRanker:
    def rank_batch(self, match_results):
        """
        match_results = [
            {
                "resume_id" : "...",
                "name": "...",
                "score": 0.74,
                "details": {...}
        """
        # Sort by score (descending)
        ranked = sorted(
            match_results,
            key=lambda x:x["score"],
            reverse=True
        )

        # Add rank index
        for idx, r in enumerate(ranked, start=1):
            r["rank"] = idx

        return ranked

