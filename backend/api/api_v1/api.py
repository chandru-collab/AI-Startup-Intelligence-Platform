from fastapi import APIRouter
from api.api_v1 import startups

api_router = APIRouter()

# Placeholder for actual routes
@api_router.get("/health")
def health_check():
    return {"status": "ok"}

api_router.include_router(startups.router, prefix="/startups", tags=["startups"])
