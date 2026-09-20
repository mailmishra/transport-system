FROM python:3.12-slim

WORKDIR /srv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY backend/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY backend/ ./
COPY concept/ ../concept/

EXPOSE 8000

CMD ["sh", "-c", "echo \"DEBUG: DATABASE_URL is set: $([ -n \"$DATABASE_URL\" ] && echo yes || echo no), host: $(echo \"$DATABASE_URL\" | sed -E 's#.*@##' | cut -d/ -f1)\" && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
