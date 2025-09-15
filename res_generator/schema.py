from pydantic import BaseModel, HttpUrl, field_validator, EmailStr
from typing import List, Optional

class Header(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    email: EmailStr | None = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None

class ExperienceItem(BaseModel):
    role: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    bullets: Optional[List[str]] = None

class ProjectItem(BaseModel):
    title: str
    skills: Optional[List[str]] = None
    bullets: Optional[List[str]] = None

class Skills(BaseModel):
    languages: Optional[List[str]] = None
    data_viz: Optional[List[str]] = None
    cloud_tools: Optional[List[str]] = None
    ai_tools: Optional[List[str]] = None
    competencies: Optional[List[str]] = None

class EducationItem(BaseModel):
    degree: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    school: Optional[str] = None
    location: Optional[str] = None

class ResumeData(BaseModel):
    header: Optional[Header] = None
    summary:Optional[str] = None
    experience: Optional[List[ExperienceItem]] = None
    projects: Optional[List[ProjectItem]] = None
    skills: Optional[Skills] = None
    education: Optional[List[EducationItem]] = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_to_none(cls, v):
        return None if v in ("", [], {}) else v
