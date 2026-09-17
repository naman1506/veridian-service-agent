from ..models import Decision
class NullProvider:
    def enrich(self, decision: Decision, chunks: list[dict]) -> Decision:
        return decision
