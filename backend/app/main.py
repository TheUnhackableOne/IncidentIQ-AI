"""IncidentIQ Backend Application Entry Point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import Settings
from app.observability.logging import setup_logging


# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events (startup/shutdown)."""
    logger.info("IncidentIQ Backend starting up...")
    yield
    logger.info("IncidentIQ Backend shutting down...")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure FastAPI application.
    
    Args:
        settings: Application settings. If None, Settings() is used.
    
    Returns:
        Configured FastAPI application.
    """
    if settings is None:
        settings = Settings()
    
    app = FastAPI(
        title="IncidentIQ API",
        description="AI-Powered Incident Investigation Platform",
        version="0.1.0",
        lifespan=lifespan,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    from app.api import routes
    app.include_router(routes.router)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return app


# Application instance
app = create_app()
