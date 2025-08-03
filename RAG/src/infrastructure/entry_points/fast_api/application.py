from fastapi import FastAPI
from src.infrastructure.entry_points.fast_api.base import set_routes
from src.applications.settings.container import get_deps_container


def include_router(app_: FastAPI, prefix: str = ""):
    """Include all routes in the FastAPI application."""
    app_.include_router(set_routes(prefix))


def create_application():
    """Create the FastAPI application."""
    container = get_deps_container()
    app_ = FastAPI()
    app_.container = container
    include_router(app_, prefix=container.app_config.url_prefix)
    return app_
