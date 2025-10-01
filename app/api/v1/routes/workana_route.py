from fastapi import APIRouter, Depends, Header, HTTPException, status
from app.services.workana_service import WorkanaService
from app.dependencies import get_workana_service
from app.schemas.freelancer_schema import FreelancerBase

workana_route_v1 = APIRouter(prefix="/api/v1/workana", tags=["Workana"])

@workana_route_v1.post("/search/freelancer")
def search_freelancer(job: str = Header(...), service: WorkanaService = Depends(get_workana_service)):
    try:
        service.navigate_to_freelancer_jobs_page()
        if service.div_cookies_exist():
            service.click_accept_cookies()
        service.set_text_search_job(job)
        service.click_seach_job()
        search_return_result = service.card_job_exist(1)
        if not search_return_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No projects were found that match your search criteria."
            )
        list_jobs: list[FreelancerBase] = service.get_all_jobs()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(err)}"
        )