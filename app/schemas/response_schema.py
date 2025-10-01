from pydantic import BaseModel, Field
from .freelancer_schema import FreelancerBase

class ResponseSearchJobs(BaseModel):
    quantity_jobs: int = Field(..., description="Total number of jobs found")
    jobs: list[FreelancerBase] = Field(default_factory=list, description="List of jobs found")