"""
JobPilot AI — FastAPI Application Entry Point

Main application with middleware, CORS, routes, and startup/shutdown events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.database import create_tables
from app.models import *  # noqa: F401, F403 — Register all models

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # --- Startup ---
    print(f"[*] Starting {settings.app_name}...")
    await create_tables()
    print("[OK] Database tables created.")

    # Seed demo data on first run
    from app.seed import seed_demo_data
    await seed_demo_data()
    print("[OK] Demo data seeded.")

    yield

    # --- Shutdown ---
    print(f"[*] Shutting down {settings.app_name}...")


app = FastAPI(
    title=settings.app_name,
    description="One profile. Multiple job portals. Smarter applications.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if settings.debug:
        import traceback
        traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred.", "success": False},
    )


# --- Mount API Routes ---
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.jobs import router as jobs_router

app.include_router(auth_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")


# --- Health Check ---
@app.get("/api/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": "0.1.0",
        "environment": settings.app_env,
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "name": settings.app_name,
        "tagline": "One profile. Multiple job portals. Smarter applications.",
        "docs": "/docs",
        "health": "/api/health",
    }
