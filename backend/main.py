from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.api_v1.api import api_router
from api.api_v1.websockets import websocket_router
from core.scheduler import setup_scheduler

# Use lifespan context manager for startup/shutdown in modern FastAPI
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

from api.api_v1.websockets import websocket_router, get_main_loop

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing APScheduler...")
    setup_scheduler()
    # Capture main event loop for websockets
    get_main_loop()
    yield
    # Shutdown actions
    logger.info("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(websocket_router) # Include websocket router

@app.get("/")
def root():
    return {"message": "Welcome to the AI Startup Intelligence Platform API"}
