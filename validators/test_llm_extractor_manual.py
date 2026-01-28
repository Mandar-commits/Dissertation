from core.llm_extractor import LLMEntityExtractor
from core.ingestion import ingest_resume

if __name__ == "__main__":
    text = ingest_resume("cv1.docx")
    extractor = LLMEntityExtractor()
    entities = extractor.extract(text)

    print("===== Extracted Entities ========")
    print(entities.to_dict())
