from pydantic import BaseModel
from datetime import date

class FreelancerBase(BaseModel):
    title: str
    about: str
    author: str
    budget: str
    stars: str
    skills: list[str]
    link: str
    # publish_date: date