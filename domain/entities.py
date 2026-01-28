from dataclasses import dataclass, field
from typing import List, Optional
import json

@dataclass
class ResumeEntities:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    current_role: Optional[str] = None
    total_years_experience: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    education: List[str] = field(default_factory=list)
    experience: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)

    @staticmethod
    def from_json(text: str):
        data = json.loads(text)
        return ResumeEntities(**data)

    def to_dict(self):
        return self.__dict__