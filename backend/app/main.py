from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.mongo import ensure_indexes
from app.routers import apartments, auth, contractors, dashboard, events, health, properties, public, tickets


@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_indexes()
    yield


app = FastAPI(
    title="ImmoFix API",
    description="REST-API für Reparatur- und Wartungsanfragen in Mietwohnungen.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(public.router, prefix="/api")
app.include_router(properties.router, prefix="/api")
app.include_router(apartments.router, prefix="/api")
app.include_router(contractors.router, prefix="/api")
app.include_router(tickets.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


@app.get("/")
def root():
    return {"name": settings.app_name, "docs": "/docs", "health": "/api/health"}
