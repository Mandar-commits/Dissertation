import logging
import requests
import json, re

from domain.entities import ResumeEntities
from utils.retry import retry_with_backoff
from config import LOCAL_LLM_MODEL, OLLAMA_BASE_URL
from core.section_extractor import SectionExtractor

logger = logging.getLogger(__name__)

_global_model = None

# Robust JSON Cleaner
def _clean_llm_json(text:str) -> str:
    if not text:
        return None

    text = text.strip()

    # remove code blocks
    text = re.sub(r"```json", "", text, flags=re.I)
    text = re.sub(r"```", "", text)

    # find FIRST {
    start = text.find("{")

    # find LAST }
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    json_text = text[start:end + 1]

    return json_text.strip()

# Safe Fallback Parser
def fallback_parse(text: str):

    logger.warning("Using fallback JSON parser")

    result = {}

    def extract_list(field):
        pattern = rf'"{field}"\s*:\s*\[(.*?)\]'
        match = re.search(pattern, text, re.S)

        if not match: return []
        items = match.group(1).split(",")
        return [i.strip().replace('"',"") for i in items]

    result["skills"] = extract_list("skills")
    result["education"] = extract_list("education")
    result["projects"] = extract_list("projects")
    result["experience"] = extract_list("experience")
    return result

# Safe JSON Loader
def safe_json_load(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logger.warning("JSON decode failed, attempting fallback")
        return fallback_parse(text)

# Token Estimation
def estimate_tokens(text):
    return len(text.split()) * 1.3

# Main LLM Extractor
class LLMEntityExtractor:
    def __init__(self, model: str = None):
        global _global_model

        if _global_model is None:
            _global_model = model or LOCAL_LLM_MODEL

        self.model = _global_model

    # Public Extraction Function
    def extract(self, text: str) -> ResumeEntities:

        sections = SectionExtractor.extract_all_sections(text)
        print(f"\nSections created : {sections}")
        prompt = self._build_semantic_prompt(sections)
        print(f"\n Prompt Generated : {prompt}")
        print(f"\nEstimated Tokens: {estimate_tokens(prompt)}")

        print("\nCalling Sematic LLM")
        response = retry_with_backoff(
            lambda : self._call_llm(prompt),
            retries=2,
            delay=2,
        )

        clean = _clean_llm_json(response)
        data = safe_json_load(clean) if clean else {}
        header = self.extract_header(text)
        return ResumeEntities(
            name=data.get("name", [None])[0] if data.get("name") else None,
            total_years_experience=data.get("total_years_of_experience"),
            skills=data.get("skills", []),
            education=data.get("education", []),
            projects=data.get("projects", [])
        )

    # Header Extraction
    def extract_header(self, text):

        email = re.findall(r"[\w.-]+@[\w.-]+", text)
        phone = re.findall(r"(\+?\d[\d\s-]{8,}\d)", text)
        print(f"Email : {email} \n Phone : {phone}")
        name = None

        for line in text.split("\n")[:5]:
            line = line.strip()
            if re.match(r"^[A-Z][a-z]+\s[A-Z][a-z]+$", line):
                name = line
                break

        role_match = re.findall(
            r"(data scientist|software engineer|developer|analyst)",
            text.lower()
        )
        role = role_match[0] if role_match else None
        return {
            "name": name,
            "email": email[0] if email else None,
            "phone": phone[0] if phone else  None,
            "current_role": role,
        }

    # Prompt Builder
    def _build_semantic_prompt(self, sections):

        return f"""
    Return ONLY valid JSON.
    
    DO NOT return nested objects.
    DO NOT return explanations.
    DO NOT return keys like university, year, board, qualification_year
    ONLY return arrays of plain strings
    
    Return exactly this format:
    
    {{
    "name": ["name of the candidate"]
    "experience": ["total experience duration only"],
    "education": ["degree names only"],
    "projects": ["project titles only"],
    "skills": ["skill names only"]
    }}
    
    Extract from sections below:
    
    WORK EXPERIENCE:
    {sections["work_experience"]}
    
    EDUCATION:
    {sections["education"][:400]}
    
    PROJECTS:
    {sections["projects"][:400]}
    
    SKILLS:
    {sections["skills"]}
    """

    # LLM Call
    def _call_llm(self, prompt: str) -> str:
        logger.debug("Calling Ollama (hybrid)")
        print("Calling Ollama")

        r = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.0,
                    "num_predict": 1200,
                    "top_p": 0.8,
                    "num_ctx": 1024,
                    "num_thread": 8,
                },
            },
        )

        r.raise_for_status()
        data = r.json()
        print("\nRESPONSE LENGTH", len(data["response"]))
        print("\nRAW LLM Response:\n", data["response"])
        return data.get("response", "").strip()