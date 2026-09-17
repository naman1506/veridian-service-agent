def classify(text: str) -> str:
    lower = text.lower()
    for keyword, category in [("phishing", "security"),("vpn", "network"),("laptop", "hardware"),("printer", "printer"),("mailbox", "email"),("expense", "expense access"),("guest", "network"),("software", "software"),("extension", "software")]:
        if keyword in lower: return category
    return "unknown"
