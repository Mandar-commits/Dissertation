import logging
import requests
import json, re

from domain.entities import ResumeEntities
from utils.retry import retry_with_backoff
from config import LOCAL_LLM_MODEL, OLLAMA_BASE_URL
from core.chunk_selector import ChunkSelector

logger = logging.getLogger(__name__)

class LLMEntityExtractor:
    def __init__(self, model: str = None):
        self.model = model or LOCAL_LLM_MODEL
        self.chunk_selector = ChunkSelector()

    # Public API
    def extract(self, text: str) -> ResumeEntities:
        logger.info("Starting HYBRID entity extraction")
        print("\nStarting HYBRID entity extraction")

        header = self._extract_header_fields(text)
        logger.debug(f"Header fields: {header}")
        print(f"\nHeader Fields: {header}")

        relevant_chunks = self.chunk_selector.select_relevant_chunks(text)
        logger.debug(f"Selected {len(relevant_chunks)} relevant chunks")
        print(f"\nSelected {len(relevant_chunks)} relevant chunks")

        print("\nCalling Sematic LLM")
        semantic_json = retry_with_backoff(
            lambda : self._call_llm(self._build_semantic_prompt(header, relevant_chunks)),
            retries=2,
            delay=2,
        )

        if not semantic_json.strip():
            raise RuntimeError("LLM returned empty response for sematic fields")

        try:
            semantic_data = json.loads(semantic_json)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse LLM JSON")
            logger.error(semantic_json)
            raise RuntimeError("Invalid JSON from LLM") from e

        logger.debug(f"Raw semantic JSON: {semantic_json}")
        print(f"\n Raw semantic JSON: {semantic_json}")

        data = {**header, **semantic_data}
        return ResumeEntities(**data)

    # Header Extraction
    def _extract_header_fields(self, text: str) -> dict:
        print("Extracting Email and Phone")
        email = re.findall(r"[\w.-]+@[\w.-]+", text)
        phone = re.findall(r"(\+?\d[\d\s-]{8,}\d)", text)
        print(f"Email : {email} \n Phone : {phone}")

        print("Extracting Name")
        name = None
        first_lines = text.strip().splitlines()[:5]
        for line in first_lines:
            l = line.strip()
            if 3 < len(l) < 40 and l.replace(" ", "").isalpha():
                name = l
                break
        print(f"Extracted Name: {name}")

        years = re.findall(r"(\d+(?:\.\d+)?)\s*(?:years|yrs)", text.lower())
        years = float(years[0]) if years else None
        print(f"Extracted Years: {years}")

        role = None
        role_matches = re.findall(r"(software engineer|data scientist|ml engineer|developer|analyst)", text.lower())
        if role_matches:
            role = role_matches[0]
        print(f"Role found in the given section: {role}")

        return {
            "name": name,
            "email": email[0] if email else None,
            "phone": phone[0] if phone else None,
            "current_role": role,
            "total_years_experience": years,
        }

    # Prompt Builder
    def _build_semantic_prompt(self, header: dict, chunks: list[str]) -> str:
        joined_chunks = "\n\n".join(f"[SECTION]\n{c}" for c in chunks)
        print("Joined the Chunks and not returning the Sematic Prompt altogether")

        return f"""
    You are given:
    1) Header info already extracted
    2) Relevant resume sections
    
    Return VALID JSON ONLY. No markdown. No explanations
    
    Header:
    {json.dumps(header, indent=2)}
    
    Relevant Sections:
    {joined_chunks}
    
    Extract only these fields:
    - skills (list of strings)
    - experience (list of strings)
    - projects (list of strings)
    - certifications (list of strings)
    """.strip()

    def _call_llm(self, prompt: str) -> str:
        logger.debug("Calling Ollama (hybrid)")
        print("Calling Ollama")

        r = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0,
                    "num_predict": 250,
                    "num_ctx": 2048,
                    "top_p": 0.9,
                    "stop": ["}\n"]
                },
            },
            timeout=120,
        )

        r.raise_for_status()
        data = r.json()

        return data.get("response", "").strip()