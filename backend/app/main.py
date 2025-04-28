from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from business.clients.fhir_client import fhir_client
from config.logger import setup_logging
from config.settings import get_settings
from presentation.routers import health
from presentation.routers.v1 import medical_qa_assistant, patients, conditions, encounters

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    fhir_client.initialize()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(medical_qa_assistant.router, prefix="/api/v1", tags=["Medical QA Assistant"])
app.include_router(patients.router, prefix="/api/v1", tags=["Patients"])
app.include_router(encounters.router, prefix="/api/v1", tags=["Encounters"])
app.include_router(conditions.router, prefix="/api/v1", tags=["Conditions"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
