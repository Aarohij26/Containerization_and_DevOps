# ─────────────────────────────────────────────
# Stage 1 – builder
#   Installs all Python deps into a virtual env
#   so only the venv is copied to the runtime stage.
# ─────────────────────────────────────────────
FROM python:3.12-alpine AS builder

# Build-time deps for compiling any C extensions
RUN apk add --no-cache gcc musl-dev libpq-dev

WORKDIR /build

# Copy only requirements first → better layer caching
COPY requirements.txt .

# Create isolated venv and install deps
RUN python -m venv /build/venv && \
    /build/venv/bin/pip install --upgrade pip --quiet && \
    /build/venv/bin/pip install --no-cache-dir -r requirements.txt


# ─────────────────────────────────────────────
# Stage 2 – runtime
#   Minimal image; no compiler toolchain.
# ─────────────────────────────────────────────
FROM python:3.12-alpine AS runtime

# Runtime lib for psycopg2
RUN apk add --no-cache libpq

# Non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy the pre-built venv from builder
COPY --from=builder /build/venv /app/venv

# Copy application source
COPY main.py .

# Make the venv the active Python environment
ENV PATH="/app/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Drop to non-root
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=3 \
    CMD wget -qO- http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
