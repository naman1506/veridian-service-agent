from .ingest import tickets
def lookup(text: str) -> list[str]:
    low = text.lower(); matches=[]
    for t in tickets():
        words = set(t["issue"].lower().split())
        if len(words & set(low.split())) >= 1: matches.append(t["id"])
    return matches[:3]
