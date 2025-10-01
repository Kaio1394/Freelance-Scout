from pydantic import BaseModel

class FreelancerBase(BaseModel):
    title: str
    about: str
    author: str
    budget: str
    stars: str
    skills: list[str]