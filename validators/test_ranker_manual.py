from core.batch_ranker import rank_resume_against_jd
from core.llm_extractor import LLMEntityExtractor
from core.ingestion import ingest_resume

extractor = LLMEntityExtractor()

print("\nSending the JD file for entity extraction")
jd_text = ingest_resume("jd1.pdf")
jd_entities = extractor.extract(jd_text)

resume_files = [
    "cv1.pdf",
    "cv1.docx",
]

resumes = []
print("Starting the Loop to extract entities from Resumes")
for r in resume_files:
    text = ingest_resume(r)
    resumes.append(extractor.extract(text))

ranked = rank_resume_against_jd(resumes, jd_entities)

for r in ranked:
    print(r["rank"], r["name"], r["score"])