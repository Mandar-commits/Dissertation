import re
import logging
import time
from weakref import finalize

from domain.entities import ResumeEntities
from core.skill_taxonomy import extract_skills_fast
from core.llm_extractor import LLMEntityExtractor
import dateparser
from datetime import datetime
from utils.performance_tracker import PerformanceTracker
from core.section_extractor import SectionExtractor

logger = logging.getLogger(__name__)

class UltraFastExtractor:
    '''
    Hybrid Resume Extractor
    Fast path:
        Regex + Skill Taxonomy + Date parsing
    Fallback:
        LLM extraction for semantic fields
    Includes performance tracking
    '''

    def __init__(self, llm_fallback=True):
        self.llm = LLMEntityExtractor()
        self.llm_fallback = llm_fallback

    # Experience Calculation using Dateparser
    def calculate_experience(self, text, llm_data=None):
        '''
        Calculate Experience using Sections
        :param text:
        :return:
        '''
        sections = SectionExtractor.extract_all_sections(text)
        work_section = sections.get("work_experience", "")

        # First - Date Ranges
        exp = self._calculate_from_dates(work_section)
        if exp:
            return exp

        # Second - Explicit durations
        exp = self._calculate_from_duration(work_section)
        if exp:
            return exp

        # Last - LLM Fallback
        if llm_data and llm_data.experience:
            exp = self._calculate_from_duration_list(llm_data.experience)
            if exp:
                return exp
            return None


        #Match Formats
        # 10/02/2025 to Present
        # 10/06/2024 to 08/02/2025
        # From 12/06/2017 to 20/01/2021

    def _calculate_from_dates(self, text):
        total_days = 0
        pattern = r"(\d{1,2}/\d{1,2}/\d{4})\s*(?:to|-|–)\s*(Present|\d{1,2}/\d{1,2}/\d{4})"
        matches = re.findall(pattern, text, re.I)

        for start, end in matches:
            start_date = dateparser.parse(start)
            if not start_date:
                continue
            if end.lower() == "present":
                end_date = datetime.now()
            else:
                end_date = dateparser.parse(end)

            if not end_date:
                continue
            delta = end_date - start_date
            total_days += delta.days
        if total_days == 0:
            return None
        total_years = total_days / 365.25
        return round(total_years, 2)

    def _calculate_from_duration(self,text):
        pattern = r"(\d+(?:\.\d+)?)\s*(years?|months?)"
        matches = re.findall(pattern, text, re.I)
        total_months = 0

        for value, unit in matches:
            value = float(value)
            if "year" in unit.lower():
                total_months += value * 12
            else:
                total_months += value
        if total_months:
            return round(total_months / 12, 2)
        return None

    def _calculate_from_duration_list(self,exp_list):
        total_months = 0
        for exp in exp_list:
            match = re.search(r"(\d+(?:\.\d+)?)\s*(years?|months?)", exp, re.I)
            if match:
                value = float(match.group(1))
                unit = match.group(2)

                if "year" in unit.lower():
                    total_months += value * 12
                else:
                    total_months += value
        if total_months:
            return round(total_months/12, 2)

        return None




    # Main Extraction Pipeline
    def extract(self, text):

        tracker = PerformanceTracker()
        tracker.metrics.text_length = len(text)
        logger.info("UltraFast execution Step")

        email = re.findall(r"[\w.-]+@[\w.-]+", text)
        phone = re.findall(r"(\+?\d[\d\s-]{8,}\d)", text)
        name = None

        for line in text.split("\n")[:5]:
            if re.match(r"^[A-Z][a-z]+\s[A-Z][a-z]+$", line.strip()):
                name = line.strip()
                break
        skills = extract_skills_fast(text)

        # Performance Parameters
        tracker.mark_fast_path()
        llm_start = time.time()
        llm_data = self.llm.extract(text)
        tracker.mark_llm(llm_start)

        experience = self.calculate_experience(text, llm_data)

        print("LLM DATA DEBUG:")
        print("Skills: ", llm_data.skills)
        print("Work Experience", experience)
        print("Education: ", llm_data.education)
        print("Projects: ", llm_data.projects)

        entity = ResumeEntities(
            name= name or llm_data.name,
            email= email[0] if email else None,
            phone=phone[0] if phone else None,
            total_years_experience=experience or llm_data.total_years_experience,
            current_role=llm_data.current_role,
            skills=skills or llm_data.skills,
            education=llm_data.education or [],
            projects=llm_data.projects or [],
        )
        metrics = tracker.finalize()
        print(metrics)

        print("\n============PERFORMANCE METRICS ===========")
        print(f"Text Length: {metrics.text_length}")
        print(f"Total Time: {metrics.total_time:.2f} sec")
        print(f"Fast Path Time: {metrics.fast_path_time:.2f} sec")
        print(f"LLM Time: {metrics.llm_time:.2f} sec")
        print(f"LLM Called: {metrics.llm_called}")
        print("=======================\n")

        return entity

