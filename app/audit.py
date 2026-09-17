from __future__ import annotations
import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from .models import Decision
ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit" / "decisions.jsonl"
DB = ROOT / "data" / "veridian.db"

def record(case: dict, retrieved: list[dict], decision: Decision):
    AUDIT.parent.mkdir(exist_ok=True)
    entry = {"timestamp":datetime.now(timezone.utc).isoformat(), "input":case, "retrieved_chunks":[x["id"] for x in retrieved], "reasoning_trace":decision.reasoning_trace, "decision":decision.model_dump()}
    with AUDIT.open("a", encoding="utf-8") as f: f.write(json.dumps(entry) + "\n")
    with sqlite3.connect(DB) as con:
        con.execute("CREATE TABLE IF NOT EXISTS decisions(case_id TEXT PRIMARY KEY, payload TEXT NOT NULL, created_at TEXT NOT NULL)")
        con.execute("INSERT OR REPLACE INTO decisions VALUES (?, ?, ?)", (decision.case_id, json.dumps(decision.model_dump()), entry["timestamp"]))

def read_audit(limit=100):
    if not AUDIT.exists(): return []
    return [json.loads(x) for x in AUDIT.read_text(encoding="utf-8").splitlines()[-limit:]]
