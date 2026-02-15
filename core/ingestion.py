import logging, PyPDF2
from docx import Document
from pdf2image import convert_from_path
import pytesseract, tempfile, os
import re
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,;:@()\-+/ ]', '', text)
    return text.strip()

def _ocr_pdf(path):
    print("Switched to OCR Path")
    images = convert_from_path(path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    print("Successfully extracted text from the output")
    return text

def ingest_resume(file):
    logger.info("Ingesting Resume")
    text = ""
    if isinstance(file, str):
        if file.lower().endswith(".pdf"):
            #print("PDF File Detected")
            with open(file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "".join(p.extract_text() or "" for p in reader.pages)
            if len(text.strip()) < 50:
                #print("\nWent for OCR Path\n")
                text = _ocr_pdf(file)
        elif file.lower().endswith(".docx"):
            #print("Doc File Detected")
            doc = Document(file)
            text = "\n".join(p.text for p in doc.paragraphs)
    else:
        #print("Not Sure what but went to else part")
        suffix = os.path.splitext(file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.read())
            path = tmp.name
        text = ingest_resume(path)

    text = clean_text(text)
    #print(f"Extracted text length: {len(text)}")
    logger.debug(f"Extracted text length: {len(text)}")
    return text