from core.matcher import ResumeJDMatcher


def test_similarity_range():
    matcher = ResumeJDMatcher()
    score = matcher.compute_similarity(
        "python developer with ml experience",
        "looking for python ml engineer",
    )

    assert 0.0 <= score <= 1.0
