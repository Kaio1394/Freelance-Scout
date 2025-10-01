from fastapi import FastAPI
from .api.v1.routes.workana_route import workana_route_v1 
from dotenv import load_dotenv
from .core.config_loader import SELECTORS
import uvicorn

print(SELECTORS["workana"]["search_input"])

app = FastAPI(title="Freelancer Scount")

app.include_router(workana_route_v1)

# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",         # <nome_do_arquivo>:<nome_da_variável_app>
#         host="0.0.0.0",     # acessível externamente
#         port=8000,
#         reload=True         # reload automático em dev
#     )