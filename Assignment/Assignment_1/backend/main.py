from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import psycopg2.extras
import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Project Assignment 1 API", version="1.0.0")

# ── DB connection settings from environment variables ──
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "db"),
    "port":     int(os.getenv("DB_PORT", "5432")),
    "dbname":   os.getenv("POSTGRES_DB", "appdb"),
    "user":     os.getenv("POSTGRES_USER", "appuser"),
    "password": os.getenv("POSTGRES_PASSWORD", "apppassword"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def wait_for_db(retries: int = 10, delay: int = 3):
    for attempt in range(1, retries + 1):
        try:
            conn = get_connection()
            conn.close()
            logger.info("Database is ready.")
            return
        except psycopg2.OperationalError as e:
            logger.warning(f"DB not ready (attempt {attempt}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("Could not connect to the database after multiple retries.")


def create_table():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id         SERIAL PRIMARY KEY,
                    name       VARCHAR(255) NOT NULL,
                    value      TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
        conn.commit()
        logger.info("Table 'records' is ready.")
    finally:
        conn.close()


@app.on_event("startup")
def startup_event():
    wait_for_db()
    create_table()


# ── Pydantic models ──
class RecordIn(BaseModel):
    name: str
    value: Optional[str] = None


class RecordOut(BaseModel):
    id: int
    name: str
    value: Optional[str]
    created_at: str


# ── Endpoints ──

@app.get("/health", tags=["Health"])
def healthcheck():
    """Healthcheck — verifies API + DB connectivity."""
    try:
        conn = get_connection()
        conn.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unreachable: {e}")


@app.post("/records", response_model=RecordOut, status_code=201, tags=["Records"])
def insert_record(record: RecordIn):
    """Insert a new record into the database."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO records (name, value) VALUES (%s, %s) "
                "RETURNING id, name, value, created_at::text",
                (record.name, record.value),
            )
            row = cur.fetchone()
        conn.commit()
        return dict(row)
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.get("/records", response_model=List[RecordOut], tags=["Records"])
def fetch_records():
    """Fetch all records from the database."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT id, name, value, created_at::text FROM records ORDER BY id;"
            )
            rows = cur.fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
