from fastapi import APIRouter, Depends
from app.services.workana_service import WorkanaService
from app.dependencies import get_workana_service

workana_route_v1 = APIRouter(prefix="/api/v1/workana", tags=["Workana"])

@workana_route_v1.post("/search/freelancer")
def search_freelancer(service: WorkanaService = Depends(get_workana_service)):
    pass