from .models import PolicyConflict
def hardware_conflict(text: str):
    if "laptop" in text.lower() and ("3.5" in text.lower() or "3½" in text.lower()):
        return PolicyConflict(sources=["KB-03", "ASSET-POLICY"], contradiction="KB-03 permits replacement after 3 years while ASSET-POLICY sets a 4-year cycle and requires Finance sign-off for early replacement.")
    return None
