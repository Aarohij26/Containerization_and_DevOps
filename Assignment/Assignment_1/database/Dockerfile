# ─────────────────────────────────────────────
# Stage 1 – config-builder
#   Validates / preprocesses any config files
#   before they land in the final image.
#   (Demonstrates multi-stage for a DB image.)
# ─────────────────────────────────────────────
FROM alpine:3.19 AS config-builder

WORKDIR /config

# Copy SQL init script
COPY init.sql .

# Lightweight validation: ensure the file is non-empty and contains CREATE TABLE
RUN grep -q "CREATE TABLE" init.sql && \
    echo "init.sql validation passed" || \
    (echo "ERROR: init.sql missing CREATE TABLE"; exit 1)


# ─────────────────────────────────────────────
# Stage 2 – runtime
#   Uses the official postgres alpine image as
#   the base (slim + battle-tested).
#   We do NOT use it directly without a custom
#   Dockerfile — all config is applied here.
# ─────────────────────────────────────────────
FROM postgres:16-alpine AS runtime

# Labels for traceability
LABEL maintainer="project-assignment-1" \
      description="Custom PostgreSQL image for Project Assignment 1"

# Copy the validated init script into the postgres entrypoint directory.
# Any .sql file here is executed automatically on first container startup.
COPY --from=config-builder /config/init.sql /docker-entrypoint-initdb.d/init.sql

# Environment variables are supplied at runtime via docker-compose.
# Defaults below are fallbacks only — override in .env / compose file.
ENV POSTGRES_DB=${POSTGRES_DB:-appdb} \
    POSTGRES_USER=${POSTGRES_USER:-appuser} \
    POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-apppassword}

# Postgres runs as the built-in 'postgres' user (non-root) by default.
# No USER directive needed — the official image already handles this.

EXPOSE 5432

HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=5 \
    CMD pg_isready -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" || exit 1
