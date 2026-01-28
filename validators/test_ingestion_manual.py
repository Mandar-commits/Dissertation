from core.ingestion import ingest_resume

if __name__ == "__main__":
    path = "cv1.docx"
    text = ingest_resume(path)
    print("====Extracted Text Preview=======")
    print(text[:1500])
    print("\n Length:", len(text))
    with open("ingest_output.txt", "w") as f:
        f.write(text)