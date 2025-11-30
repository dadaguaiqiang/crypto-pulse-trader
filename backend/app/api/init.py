from fastapi import APIRouter
from app.api.v1 import health, markets

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(markets.router, prefix="/markets", tags=["markets"])