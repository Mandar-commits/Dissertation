import re
import logging
from domain.entities import ResumeEntities
from core.skill_taxonomy import extract_skills_fast
from core.llm_extractor import LLMEntityExtractor

logger = logging.getLogger(__name__)

class UltraFastExtractor:

    def __init__(self, llm_fallback=True):
        self.llm = LLMEntityExtractor()
        self.llm_fallback = llm_fallback

    def _estimate_work_years(self, text:str):
        matches = re.findall(r"(20\d{2})\s*[-–]\s*(20\d{2}|present)", text.lower())
        spans = []

        for start, end in matches:
            start = int(start)
            end = 2025 if end == "present" else int(end)

            if 0 < end - start <= 15:
                spans.append(end - start)
            return sum(spans) if spans else None

    # ---- Regex header extraction ------
    def _extract_header(self, text: str):

        email = re.findall(r"[\w.-]+@[\w.-]+", text)
        phone = re.findall(r"(\+?\d[\d\s-]{8,}\d)", text)

        name = None
        for line in text.splitlines()[:5:]:
            l = line.strip()
            if 3 < len(l) < 40 and l.replace(" ", "").isalpha():
                name = l
                break

        years = self._estimate_work_years(text)
        return name, email, phone, years


    # ------- Fast Extraction ---------
    def extract(self, text: str) -> ResumeEntities:

        logger.info("UltraFast execution Step")
        print("UltraFast execution Step")

        name, email, phone, years = self._extract_header(text)
        skills = extract_skills_fast(text)

        # If info is not enough go to llm
        # if skills:
        #     logger.info("Fast path success - skipping LLM")
        #     print("Fast path success - Skipping LLM")
        #
        #     return ResumeEntities(
        #         name= name,
        #         email= email[0] if email else None,
        #         phone=phone[0] if phone else None,
        #         total_years_experience=years,
        #         skills=skills
        #     )

        # Fallback
        if self.llm_fallback:
            logger.info("Fast path incomplete using hybrid LLM fallback")
            print("Fast path incomplete using hybrid LLM fallback")
            return self.llm.extract(text)

        logger.warning("Fast path incomplete - fallback disabled")
        print("Fast path incomplete - fallback disabled")
        return ResumeEntities(
            name = name,
            email= email[0] if email else None,
            phone=phone[0] if phone else None,
            total_years_experience=years,
            skills=skills
        )

