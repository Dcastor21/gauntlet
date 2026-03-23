"""
Gauntlet API — Main FastAPI application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    # Startup: verify connections
    await redis_client.ping()
    yield
    # Shutdown: close connections
    await redis_client.aclose()


app = FastAPI(
    title="Gauntlet API",
    description="Multi-Cloud LLM Evaluation & Benchmarking Platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow the Vercel frontend and local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",           # Local Next.js dev
        #"https://gauntlet.solvexis.dev",   # Production
        "https://*.vercel.app",            # Preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
async def health_check():
    """
    Health check for Render uptime monitoring.
    PRD requirement: No auth required.
    """
    return {"status": "healthy", "service": "gauntlet-api"}


# Router registration happens here as we build each module:
# from app.routers import runs, testsets, rubrics, providers, webhooks
# app.include_router(runs.router, prefix="/api/v1")
# app.include_router(testsets.router, prefix="/api/v1")
# ...
