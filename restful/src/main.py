from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from contextlib import asynccontextmanager
import logging
import time

from dotenv import load_dotenv

load_dotenv()

from .config.settings import settings
from .api.router import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Hackathon 2025 API with Slack integration")
    logger.info("Application started successfully")
    yield
    logger.info("Shutting down AI Hackathon 2025 API")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A modern Python API for AI Hackathon 2025 with Slack and Owl integration",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("")
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": settings.APP_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "features": [
            "Owl REST API",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
    )
