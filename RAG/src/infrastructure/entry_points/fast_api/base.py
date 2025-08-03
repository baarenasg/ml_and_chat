from fastapi import APIRouter

from src.infrastructure.entry_points.fast_api.routes import (
    rag_router
)


def set_routes(prefix_url: str = "") -> APIRouter:
    """Set all routes for the FastAPI application."""
    api_router = APIRouter(prefix=prefix_url)
    api_router.include_router(
        rag_router.router, prefix="/api", tags=["api"]
    )
    return api_router
