from .models import Decision
def validate(decision: Decision) -> Decision:
    if not decision.citations:
        decision.decision = "ROUTE_TO_HUMAN"; decision.reason_code = "no_policy_coverage"; decision.owner = "IT"
        decision.override_reason = "Grounding guard: no policy citation supplied, so routing to a human."
    if decision.confidence < .75:
        decision.decision = "NEEDS_INFO" if decision.missing_fields else "ROUTE_TO_HUMAN"
        decision.override_reason = (decision.override_reason or "") + " Confidence guard applied."
    if decision.policy_conflict:
        decision.decision = "ROUTE_TO_HUMAN"; decision.reason_code = "policy_conflict"
    return decision
