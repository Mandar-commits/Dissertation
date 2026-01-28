import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class ResumeJDMatcher:
    def compute_similarity(self, resume_text: str, jd_text: str) -> float:
        logger.info("Computing resume-JD similarity")
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        logger.debug(f"Similarity Score: {score}")
        return round(float(score), 3)

