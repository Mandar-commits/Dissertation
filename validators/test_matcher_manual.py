from core.matcher import ResumeJDMatcher

if __name__ == "__main__":
    resume_text = "Python developer with ML experience"
    jd_text = "Looking for a Python ML Engineer"

    matcher = ResumeJDMatcher()
    score = matcher.compute_similarity(resume_text, jd_text)

    print("Similarity Score")
    print(score)