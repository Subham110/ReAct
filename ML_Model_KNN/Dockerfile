# STAGE 1: Builder (Installs dependencies with uv)
FROM python:3.13-slim-bookworm AS builder

# Install uv binary from official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Disable bytecode compilation and cache
ENV UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

# Clean pure unit test folders & bytecode caches (DO NOT run strip on .so files!)
RUN rm -rf /app/.venv/lib/python*/site-packages/pandas/tests \
           /app/.venv/lib/python*/site-packages/sklearn/tests \
           /app/.venv/lib/python*/site-packages/scipy/*/tests && \
    find /app/.venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -type f -name "*.pyc" -delete

# STAGE 2: Clean Production Runtime
FROM python:3.13-slim-bookworm AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/appuser \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Clean debian docs and create real home directory
RUN rm -rf /usr/share/doc /usr/share/man /var/cache/debconf/*-old && \
    addgroup --system appgroup && \
    adduser --system --ingroup appgroup --home /home/appuser appuser && \
    mkdir -p /home/appuser && chown -R appuser:appgroup /home/appuser

# Copy virtualenv from builder (zero layer duplication)
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --chown=appuser:appgroup app ./app
COPY --chown=appuser:appgroup models ./models

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')" || exit 1

# Launch using Gunicorn with 4 async Uvicorn workers
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--timeout", "60", "--access-logfile", "-"]
