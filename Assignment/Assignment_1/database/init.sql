-- init.sql
-- Runs automatically when the container starts for the first time.
-- The records table is also created by the backend on startup,
-- but having it here ensures it exists even before the backend connects.

CREATE TABLE IF NOT EXISTS records (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    value      TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
