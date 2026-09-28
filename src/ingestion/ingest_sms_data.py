from pathlib import Path
import hashlib

import psycopg


# =========================
# Configuration
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "sample_100k.txt"


# =========================
# File Hash
# =========================

def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA-256 hash for a file."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# =========================
# Database Connection
# =========================

def get_db_connection():
    """Create a connection to PostgreSQL."""
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="sms_gateway_analytics",
        user="analytics_user",
        password="analytics_password",
    )


# =========================
# Ingestion Check
# =========================

def is_file_already_loaded(conn, file_hash: str) -> bool:
    """Check whether a file hash already exists in the ingestion log."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM raw.ingestion_log
                WHERE file_hash = %s
            );
            """,
            (file_hash,),
        )

        return cur.fetchone()[0]


# =========================
# Main
# =========================

if __name__ == "__main__":
    file_path = DATA_PATH

    file_hash = calculate_file_hash(file_path)

    print(f"File: {file_path}")
    print(f"SHA-256: {file_hash}")

    conn = get_db_connection()

    try:
        already_loaded = is_file_already_loaded(
            conn,
            file_hash,
        )

        if already_loaded:
            print("Ingestion action: SKIP")
        else:
            print("Ingestion action: LOAD")

    finally:
        conn.close()