from fastapi import APIRouter, Depends, Header, HTTPException, status
from app.services.workana_service import WorkanaService
from app.dependencies import get_workana_service, get_email_service, get_excel_service
from app.schemas.freelancer_schema import FreelancerBase
import time
from app.schemas.response_schema import ResponseSearchJobs
from app.services.email_service import EmailService
from app.services.excel_service import ExcelService

workana_route_v1 = APIRouter(prefix="/api/v1/workana", tags=["Workana"])

@workana_route_v1.post("/search/freelancer/xlsx")
def search_freelancer_xlsx(path_excel: str = Header(...), tab: str = Header(...),
                    service: WorkanaService = Depends(get_workana_service), 
                    email_service: EmailService = Depends(get_email_service),
                    excel_service: ExcelService = Depends(get_excel_service)):
    try:
        if not path_excel.strip():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Header 'path_excel' is requirement."
            )
        df = excel_service.get_dataframe(path_excel, tab)
        
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(err)}"
        )

@workana_route_v1.post("/search/freelancer")
def search_freelancer(job: str = Header(...), limit_search: int = Header(...), 
                    service: WorkanaService = Depends(get_workana_service), 
                    email_service: EmailService = Depends(get_email_service)):
    list_jobs: list[FreelancerBase]
    try:
        if not job.strip():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Header 'job' is requirement."
            )
        if limit_search is None or limit_search < 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Header 'limit_search' can't be less than 1."
            )
        
        service.navigate_to_freelancer_jobs_page()
        if service.div_cookies_exist():
            service.click_accept_cookies()
        service.set_text_search_job(job)
        service.click_seach_job()
        time.sleep(5)
        search_return_result = service.card_job_exist(1)
        if not search_return_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No projects were found that match your search criteria."
            )
        if service.div_register_exist():
            service.click_close_div_register()
            
        list_jobs = service.get_all_jobs(limit=limit_search)
        html = email_service.generate_html(list_freela=list_jobs)
        
        email_service.define_credentials()
        email_service.define_configs_email()    
        connect, msg_erro = email_service.connect()
        if not connect:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {msg_erro}"
            )
        email_service.send(html=html) 
        return ResponseSearchJobs(quantity_jobs=len(list_jobs), jobs=list_jobs)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(err)}"
        )
