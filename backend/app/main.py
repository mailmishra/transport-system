from pathlib import Path

from fastapi import FastAPI, Response
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
    reports,
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
api.include_router(reports.router)
app.mount("/api", api)

# Uploaded firm logos (see routers/firms.py's MEDIA_DIR) -- must be mounted
# before the SPA catch-all below, or SPAStaticFiles' 404->index.html
# fallback would swallow /media/* requests.
MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


# The retired concept/index.html prototype (git history only -- it's no
# longer built or served, see FRONTEND_DIR below) registered a service
# worker at "/" with a cache-first fetch handler. That registration is
# permanent in any browser that loaded it before the React SPA replaced
# concept/ at this origin: it keeps intercepting navigation and serving
# its own stale cached index.html forever, regardless of what the server
# now returns, since a service worker -- once installed -- is the
# browser's source of truth for its scope until something replaces it.
# This route is that replacement: any such browser's routine SW update
# check fetches this, and it immediately unregisters itself, clears every
# cache, and reloads every open tab -- one-time cleanup, inert for anyone
# who never had the old prototype's service worker in the first place.
_SW_KILL_SWITCH = """
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => {
  event.waitUntil(
    Promise.all([
      self.registration.unregister(),
      caches.keys().then((keys) => Promise.all(keys.map((k) => caches.delete(k)))),
    ]).then(() =>
      self.clients.matchAll({ type: "window" }).then((clients) => {
        clients.forEach((client) => client.navigate(client.url));
      })
    )
  );
});
"""


@app.get("/sw.js")
async def service_worker_kill_switch():
    return Response(content=_SW_KILL_SWITCH, media_type="application/javascript")


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
