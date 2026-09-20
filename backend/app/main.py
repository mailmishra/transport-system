from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routers import bilties, firms, loading_slips

settings = get_settings()

app = FastAPI(title="Transport Management System API")

if settings.cors_origin_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api = FastAPI(title="Transport Management System API")
api.include_router(firms.router)
api.include_router(loading_slips.router)
api.include_router(bilties.router)
app.mount("/api", api)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


# Serve the existing concept/ frontend as-is; backend/ and concept/ are
# siblings in the repo.
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "concept"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
