import json
from app.orchestrator import Orchestrator
from app import ingest

def test_golden_set():
    golden=json.load(open('data/golden_set.json'))
    o=Orchestrator()
    assert {case: o.run(case).decision for case in golden} == golden
def test_grounding_guard_applies_to_empty_citation():
    d=Orchestrator().run('REQ-15')
    assert d.decision == 'NEEDS_INFO'
    assert d.override_reason
def test_conflict_is_explicit():
    d=Orchestrator().run('REQ-01')
    assert d.policy_conflict and set(d.policy_conflict.sources)=={'KB-03','ASSET-POLICY'}
def test_ask_refuses_unknown_policy():
    r=Orchestrator().ask('Nimbus reciprocal quantum access policy')
    assert r['citations']==[] and 'Not covered' in r['answer']
