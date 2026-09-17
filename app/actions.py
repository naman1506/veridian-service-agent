from .models import Decision
def execute(decision: Decision) -> list[str]:
    # Deliberately records proposed actions only. This demo has no authority to touch production systems.
    return decision.actions_taken
