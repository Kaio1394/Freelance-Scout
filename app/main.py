from fastapi import FastAPI
from app.api.v1.routes.workana_route import workana_route_v1 
from dotenv import load_dotenv
from app.core.config_loader import SELECTORS

print(SELECTORS["workana"]["search_input"])

app = FastAPI(title="Freelancer Scount")

app.include_router(workana_route_v1)