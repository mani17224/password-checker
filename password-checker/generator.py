import secrets
import string


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Generate a cryptographically secure password using secrets module.
    Guarantees at least one character from each enabled character set.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4")

    pool = string.ascii_lowercase
    required_chars = [secrets.choice(string.ascii_lowercase)]

    if use_uppercase:
        pool += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))

    if use_digits:
        pool += string.digits
        required_chars.append(secrets.choice(string.digits))

    if use_symbols:
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        pool += symbols
        required_chars.append(secrets.choice(symbols))

    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(pool) for _ in range(remaining_length)]

    # Shuffle to prevent required chars from always appearing at the start
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def generate_passphrase(word_count: int = 4) -> str:
    """
    Generate a memorable passphrase using random words.
    Example output: correct-horse-battery-staple
    """
    wordlist = [
        "apple", "bridge", "castle", "delta", "eagle", "forest",
        "globe", "harbor", "island", "jungle", "knight", "lemon",
        "mango", "noble", "ocean", "planet", "queen", "river",
        "stone", "tiger", "ultra", "valley", "winter", "xenon",
        "yellow", "zebra", "alpha", "brave", "crane", "dance"
    ]
    words = [secrets.choice(wordlist) for _ in range(word_count)]
    separator = secrets.choice(["-", "_", ".", "#"])
    return separator.join(words)