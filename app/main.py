from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.identity.routers.auth_router import router as auth_router
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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://167.172.101.54",
            "http://167.172.101.54:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["Health"])
    async def health():
        return {
            "status": "ok",
            "service": settings.app_name,
            "version": settings.app_version,
        }

    app.include_router(auth_router)
    app.include_router(brand_router)

    return app


app = create_app()