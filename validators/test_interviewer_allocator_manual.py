from core.interviewer_allocator import InterviewerAllocator

if __name__ == "__main__":
    allocator = InterviewerAllocator()

    candidates = [
        {"name": "Alice"},
        {"name": "Bob"},
        {"name": "Carol"},
    ]

    interviewers = ["I1", "I2"]

    assignments = allocator.assign(candidates, interviewers)

    print("Interviewer Assignment")
    print(assignments)