# Stage 1: build the React/Vite frontend. concept/index.html is retired;
# the built SPA is what FastAPI serves at "/" from here on.
FROM node:20-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: the Python backend, unchanged, plus the built frontend.
FROM python:3.12-slim
WORKDIR /srv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY backend/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY backend/ ./
COPY --from=frontend-build /app/frontend/dist ../frontend_dist/

EXPOSE 8000

# Demo-data seeding (app/scripts/seed_demo_data.py) is gated by the
# SEED_DEMO_DATA env var (off by default -- see app/config.py) and always
# exits 0 even on failure, so `|| true` here is belt-and-suspenders: a
# seeding problem must never be able to stop the app from starting.
CMD ["sh", "-c", "alembic upgrade head && (python -m app.scripts.seed_demo_data || true) && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
