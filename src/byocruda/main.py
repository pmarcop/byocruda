from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Dict, Any

from byocruda.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup operations
    print(f"Starting {settings.api.project_name} API...")
    print(f"Debug mode: {settings.api.debug}")
    # Here we'll later add:
    # - Database connection
    # - Cache initialization
    # - Background tasks startup
    yield
    # Shutdown operations
    print("Shutting down API...")
    # Here we'll later add:
    # - Database connection closure
    # - Cache cleanup
    # - Background tasks shutdown

def create_application() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    """
    app = FastAPI(
        title=settings.api.project_name,
        description=settings.api.description,
        version=settings.api.version,
        docs_url="/docs" if settings.api.debug else None,
        redoc_url="/redoc" if settings.api.debug else None,
        openapi_url="/openapi.json" if settings.api.debug else None,
        lifespan=lifespan,
        debug=settings.api.debug
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Modify this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add exception handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                }
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": 500,
                    "message": "Internal Server Error",
                    "detail": str(exc) if settings.api.debug else "An unexpected error occurred"
                }
            },
        )

    # Root endpoint
    @app.get("/", response_model=Dict[str, Any])
    async def root():
        """Root endpoint returning basic API information."""
        return {
            "message": f"Welcome to {settings.api.project_name} API",
            "version": settings.api.version,
            "status": "operational",
            "docs": "/docs" if settings.api.debug else "Documentation disabled in production",
        }

    # Health check endpoint
    @app.get("/health", response_model=Dict[str, Any])
    async def health_check():
        """Health check endpoint for monitoring."""
        return {
            "status": "healthy",
            "version": settings.api.version,
            "api": {
                "name": settings.api.project_name,
                "debug": settings.api.debug
            }
        }

    return app

# Create the application instance
app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.api.debug
    )
