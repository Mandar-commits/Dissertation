from core.fast_extractor import UltraFastExtractor
from core.ingestion import ingest_resume

if __name__ == "__main__":
    text = ingest_resume("cv1.docx")

    extractor = UltraFastExtractor()
    entities = extractor.extract(text)

    print("===== Extracted Entities ========")
    print(entities.to_dict())
