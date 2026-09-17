from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

DecisionKind = Literal["AUTO_RESOLVE", "NEEDS_INFO", "ROUTE_TO_HUMAN", "FLAG_RISK", "MONITOR"]
ReasonCode = Literal["policy_conflict", "no_policy_coverage", "needs_approval", "missing_information", "other_team_owns", "security_violation", "within_sla"]
Owner = Literal["IT", "IT Security", "Manager", "Finance", "Employee"]

class PolicyConflict(BaseModel):
    sources: list[str]
    contradiction: str

class Decision(BaseModel):
    case_id: str
    case_type: Literal["request", "ticket", "adversarial"] = "request"
    employee: str
    category: str
    urgency: Literal["low", "normal", "high", "critical"] = "normal"
    decision: DecisionKind
    reason_code: ReasonCode
    citations: list[str] = Field(default_factory=list)
    policy_conflict: PolicyConflict | None = None
    precedent: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    owner: Owner = "IT"
    sla_due: str | None = None
    age_business_days: int = 0
    is_stale: bool = False
    confidence: float = 0.9
    reasoning_trace: list[str] = Field(default_factory=list)
    draft_reply: str
    actions_taken: list[str] = Field(default_factory=list)
    override_reason: str | None = None

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    citations: list[str]
