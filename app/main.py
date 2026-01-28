from app.logging_config import setup_logging
from core.ingestion import ingest_resume
from core.llm_extractor import LLMEntityExtractor
from core.section_pipeline import process_resume
from core.matcher import ResumeJDMatcher
from core.ranker import CandidateRanker
from core.interviewer_allocator import InterviewerAllocator
from utils.feedback_generator import generate_feedback

setup_logging()
text = ingest_resume("data/cv1.pdf")
extractor = LLMEntityExtractor()
entities = process_resume(extractor.extract(text))
matcher = ResumeJDMatcher()
similarity = matcher.compute_similarity(text, text)
ranker = CandidateRanker()
score = ranker.rank(similarity, len(entities.skills), len((entities.projects)))
feedback = generate_feedback(entities, similarity)
allocator = InterviewerAllocator()
assignments = allocator.assign([entities.to_dict()], ["Alice", "Bob"])
print(score, feedback, assignments)