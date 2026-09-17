from __future__ import annotations
from . import ingest
from .retriever import Retriever
from .policy_engine import verdict
from .reasoner import enrich
from .guardrails import validate
from .audit import record
from .actions import execute

class Orchestrator:
    def __init__(self): self.retriever = Retriever()
    def run(self, case_id: str):
        case = next((x for x in ingest.cases() if x["id"] == case_id), None)
        if not case: raise KeyError(case_id)
        chunks = self.retriever.search(case["request"])
        deterministic = verdict(case)
        final = validate(enrich(deterministic, chunks))
        execute(final); record(case, chunks, final)
        return final
    def run_all(self): return [self.run(case["id"]) for case in ingest.cases()]
    def ask(self, question: str):
        chunks = self.retriever.search(question, 2)
        # Generic words such as "policy" or "access" do not establish coverage.
        if not chunks or chunks[0]["score"] < 3:
            return {"answer":"Not covered by policy. I cannot invent a policy, owner, SLA, or approval path.","citations":[]}
        top = chunks[0]
        return {"answer":f"{top['title']}: {top['text']}", "citations":[top["id"]]}
