from .llm import client
from .models import Decision
def enrich(deterministic: Decision, chunks: list[dict]) -> Decision:
    candidate = client().enrich(deterministic.model_copy(deep=True), chunks)
    # A provider may improve prose, never change the policy outcome.
    if candidate.decision != deterministic.decision:
        deterministic.override_reason = "LLM decision disagreed with deterministic policy engine. Deterministic verdict retained."
    return deterministic
