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

            r["explanation"] = self.generate_explanation(
                r["details"]
            )

        return ranked

    def generate_explanation(self, details):
        return {
            "matched_skills": details["matched_skills"],
            "missing_skills": details["missing_skills"],
            "score_breakdown": details["score_breakdown"],
            "confidence": details["confidence"]
        }

