import re
import math

COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "letmein", "admin",
    "welcome", "monkey", "dragon", "master", "hello",
    "abc123", "password1", "iloveyou", "sunshine", "princess"
]

def check_strength(password: str) -> dict:
    """
    Analyse password strength across 6 criteria.
    Returns a dict with score (0-6), level, feedback, and entropy.
    """
    if not password:
        return {"score": 0, "level": "empty", "feedback": [], "entropy": 0}

    criteria = {
        "length":   len(password) >= 12,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit":    bool(re.search(r"\d", password)),
        "symbol":   bool(re.search(r"[^a-zA-Z0-9]", password)),
        "not_common": password.lower() not in COMMON_PASSWORDS,
    }

    score = sum(criteria.values())
    e = calculate_entropy(password)

    levels = {6: "Very Strong", 5: "Strong", 4: "Fair",
              3: "Weak", 2: "Very Weak", 1: "Very Weak", 0: "Very Weak"}

    feedback = []
    if not criteria["length"]:
        feedback.append("Use at least 12 characters")
    if not criteria["uppercase"]:
        feedback.append("Add uppercase letters (A-Z)")
    if not criteria["lowercase"]:
        feedback.append("Add lowercase letters (a-z)")
    if not criteria["digit"]:
        feedback.append("Add numbers (0-9)")
    if not criteria["symbol"]:
        feedback.append("Add symbols (!@#$%...)")
    if not criteria["not_common"]:
        feedback.append("This is a commonly used password — avoid it!")

    return {
        "score": score,
        "level": levels[score],
        "criteria": criteria,
        "feedback": feedback,
        "entropy": e,
    }


def calculate_entropy(password: str) -> float:
    """
    Entropy formula: E = length * log2(pool_size)
    Higher entropy = harder to brute force.
    """
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"\d", password):    pool += 10
    if re.search(r"[^a-zA-Z0-9]", password): pool += 32

    if pool == 0:
        return 0.0
    return round(len(password) * math.log2(pool), 2)