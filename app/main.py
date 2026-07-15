from fastapi import FastAPI

from app.core.config import settings
from app.modules.reference.brands.router import router as brand_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="Production Management System for Sewing Factories",
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.get("/health", tags=["Health"])
    async def health():
        return {
            "status": "ok",
            "service": settings.app_name,
            "version": settings.app_version,
        }

    return app


app = create_app()

from app.modules.identity.routers.auth_router import router as auth_router

app.include_router(auth_router)
app.include_router(brand_router)