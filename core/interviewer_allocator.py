import logging

logger = logging.getLogger(__name__)

class InterviewerAllocator:
    def assign(self, candidates, interviewers):
        logger.info("Assigning interviewers")
        assignments = {}
        for i, c in enumerate(candidates):
            interviewer = interviewers[i % len(interviewers)]
            assignments[c['name']] = interviewer
        return assignments