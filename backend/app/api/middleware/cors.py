from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

def add_cors_middleware(app: FastAPI) -> None:
    """
    Add CORS middleware to the FastAPI application

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
        expose_headers=["Content-Disposition", "Content-Length"],
        max_age=86400,  # 24 hours
    )

    logger.info("CORS middleware configured")
    logger.debug(f"Allowed origins: {settings.allowed_origins}")
    logger.debug(f"Allowed methods: {settings.allowed_methods}")
    logger.debug(f"Allowed headers: {settings.allowed_headers}")

def configure_cors_for_production(app: FastAPI, allowed_origins: list) -> None:
    """
    Configure CORS for production environment with specific origins

    Args:
        app: FastAPI application instance
        allowed_origins: List of allowed origins for production
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers