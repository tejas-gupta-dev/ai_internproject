def should_escalate(persona, sentiment):
    if persona == "frustrated_user" and sentiment == "negative":
        return True
    return False