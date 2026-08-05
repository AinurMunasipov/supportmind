from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(title="SupportMind API", lifespan=lifespan)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "service": "SupportMind API",
        "status": "running",
    }
