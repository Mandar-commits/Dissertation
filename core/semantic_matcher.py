from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticMatcher:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def compute(self,  resume_text, jd_text):
        resume_vec = self.model.encode([resume_text])
        jd_vec = self.model.encode([jd_text])

        score = cosine_similarity(resume_vec, jd_vec)[0][0]

        return round(float(score), 3)