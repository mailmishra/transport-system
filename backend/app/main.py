from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import get_settings
from app.routers import (
    agent_payments,
    agents,
    bilties,
    firms,
    loading_slips,
    receipts,
    truck_owner_payments,
    truck_owners,
    vehicles,
)

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
api.include_router(agents.router)
api.include_router(truck_owners.router)
api.include_router(vehicles.router)
api.include_router(agent_payments.router)
api.include_router(truck_owner_payments.router)
api.include_router(receipts.router)
app.mount("/api", api)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


class SPAStaticFiles(StaticFiles):
    """Client-side routes (e.g. /bilti/<id>/edit) don't correspond to a
    real file on disk. Plain StaticFiles(html=True) only auto-serves
    index.html for "/" and real directories, so a deep-link refresh 404s
    without this: any 404 for a non-API path falls back to index.html and
    lets react-router's own routing take over from there.
    """

    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            if exc.status_code == 404:
                return await super().get_response("index.html", scope)
            raise


# The built frontend (backend/Dockerfile's frontend-build stage); backend/
# and frontend_dist/ are siblings in the container, mirroring how
# concept/ used to sit alongside backend/ in local (non-Docker) dev.
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend_dist"
if FRONTEND_DIR.exists():
    app.mount("/", SPAStaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
