from core.interviewer_allocator import InterviewerAllocator


def test_assignment_round_robin():
    allocator = InterviewerAllocator()

    candidates = [
        {"name": "Alice"},
        {"name": "Bob"},
        {"name": "Carol"},
    ]

    interviewers = ["I1", "I2"]

    assignments = allocator.assign(candidates, interviewers)

    assert assignments["Alice"] == "I1"
    assert assignments["Bob"] == "I2"
    assert assignments["Carol"] == "I1"
