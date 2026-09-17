from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load_json(name: str):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
def requests(): return load_json("requests.json")
def tickets(): return load_json("tickets.json")
def knowledge_base(): return load_json("knowledge_base.yaml")
def cases():
    active = [x for x in tickets() if "active" in x["status"].lower()]
    return requests() + [{"id":x["id"],"employee":x["employee"],"opened":"2026-09-22","request":x["issue"],"action_so_far":x["status"],"case_type":"ticket"} for x in active]
