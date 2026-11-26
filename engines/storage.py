"""SQLite persistence for normalized source observations."""
import json
import sqlite3
from pathlib import Path

DEFAULT_DB = Path("data/gmf_os.sqlite3")

def connect(db_path=DEFAULT_DB):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("""CREATE TABLE IF NOT EXISTS observations (
        observation_id TEXT PRIMARY KEY,
        series_id TEXT NOT NULL,
        source_id TEXT NOT NULL,
        value REAL NOT NULL,
        unit TEXT NOT NULL,
        observed_at TEXT NOT NULL,
        published_at TEXT,
        retrieved_at TEXT NOT NULL,
        frequency TEXT NOT NULL,
        evidence_class TEXT NOT NULL,
        quality_status TEXT NOT NULL,
        methodology_id TEXT,
        source_record_id TEXT,
        metadata_json TEXT NOT NULL
    )""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_obs_series_time ON observations(series_id, observed_at)")
    return conn

def save_observations(rows, db_path=DEFAULT_DB):
    conn = connect(db_path)
    try:
        for row in rows:
            conn.execute("""INSERT OR REPLACE INTO observations
                (observation_id,series_id,source_id,value,unit,observed_at,published_at,
                 retrieved_at,frequency,evidence_class,quality_status,methodology_id,
                 source_record_id,metadata_json)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (row["observation_id"], row["series_id"], row["source_id"], float(row["value"]),
                 row["unit"], row["observed_at"], row.get("published_at"), row["retrieved_at"],
                 row.get("frequency", "source_defined"), row["evidence_class"], row["quality_status"],
                 row.get("methodology_id"), row.get("source_record_id"),
                 json.dumps(row.get("metadata", {}), sort_keys=True)))
        conn.commit()
        return len(rows)
    finally:
        conn.close()

def latest_observations(db_path=DEFAULT_DB, limit=100):
    conn = connect(db_path)
    try:
        cur = conn.execute("""SELECT series_id,source_id,value,unit,observed_at,published_at,
            retrieved_at,frequency,evidence_class,quality_status FROM observations
            ORDER BY observed_at DESC LIMIT ?""", (int(limit),))
        columns = [x[0] for x in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        conn.close()
