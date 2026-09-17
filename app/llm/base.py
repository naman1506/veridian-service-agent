from typing import Protocol
from ..models import Decision
class LLMClient(Protocol):
    def enrich(self, decision: Decision, chunks: list[dict]) -> Decision: ...
