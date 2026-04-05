from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import branches, business_units, companies, health, settings
from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="Gondor Companies",
    description="Companies microservice for the Gondor platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router, tags=["health"])
app.include_router(companies.router, prefix="/v1", tags=["companies"])
app.include_router(business_units.router, prefix="/v1", tags=["business-units"])
app.include_router(branches.router, prefix="/v1", tags=["branches"])
app.include_router(settings.router, prefix="/v1", tags=["settings"])
