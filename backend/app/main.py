from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config.logger import setup_logging
from config.settings import get_settings
from presentation.routers import health

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
