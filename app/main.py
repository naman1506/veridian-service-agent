from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from . import ingest
from .models import AskRequest
from .orchestrator import Orchestrator
from .audit import read_audit

app = FastAPI(title="Veridian Service Agent", version="1.0.0")
engine = Orchestrator()
@app.get("/healthz")
def health(): return {"ok":True, "clock":"2026-09-25T17:00:00+05:30", "mode":"deterministic"}
@app.get("/api/cases")
def cases(): return ingest.cases()
@app.get("/api/kb")
def kb(): return ingest.knowledge_base()
@app.get("/api/cases/{case_id}")
def case(case_id: str):
    try: return engine.run(case_id)
    except KeyError: raise HTTPException(404, "Case not found")
@app.post("/api/run")
def run_all(): return [x.model_dump() for x in engine.run_all()]
@app.post("/api/run/{case_id}")
def run_one(case_id: str):
    try: return engine.run(case_id)
    except KeyError: raise HTTPException(404, "Case not found")
@app.post("/api/ask")
def ask(body: AskRequest): return engine.ask(body.question)
@app.get("/api/metrics")
def metrics():
    decisions = [engine.run(x["id"]) for x in ingest.cases()]
    total=len(decisions)
    return {"cases_processed":total,"auto_resolution_rate":round(sum(x.decision=="AUTO_RESOLVE" for x in decisions)/total,2),"escalation_rate":round(sum(x.decision=="ROUTE_TO_HUMAN" for x in decisions)/total,2),"grounding_rate":round(sum(bool(x.citations) for x in decisions)/total,2),"conflicts_detected":sum(bool(x.policy_conflict) for x in decisions),"risks_flagged":sum(x.decision=="FLAG_RISK" for x in decisions),"analyst_hours_saved":round(sum(x.decision=="AUTO_RESOLVE" for x in decisions)*0.25,1)}
@app.get("/api/audit")
def audit(): return read_audit()
app.mount("/", StaticFiles(directory="static", html=True), name="static")
