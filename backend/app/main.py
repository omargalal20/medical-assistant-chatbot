from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config.logger import setup_logging
from config.settings import get_settings
from presentation.routers import health
from presentation.routers.v1 import medical_qa_assistant

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(medical_qa_assistant.router, prefix="/api/v1", tags=["Medical QA Assistant"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
