# Password Strength Checker & Generator

A desktop Python application that analyses password strength using entropy scoring and generates cryptographically secure passwords.

## Features

- **Strength Analysis** — Scores passwords across 6 criteria with real-time feedback
- **Entropy Calculation** — Uses `E = length × log₂(pool_size)` to quantify password security
- **Secure Generator** — Uses Python's `secrets` module (cryptographically secure, not `random`)
- **Passphrase Generator** — Generates memorable multi-word passphrases
- **Clipboard Copy** — One-click copy to clipboard

## Strength Criteria

| Criterion | Requirement |
|---|---|
| Length | ≥ 12 characters |
| Uppercase | At least one A-Z |
| Lowercase | At least one a-z |
| Digit | At least one 0-9 |
| Symbol | At least one !@#$... |
| Not Common | Not in known weak passwords list |

## Entropy Guide

| Entropy | Security Level |
|---|---|
| < 28 bits | Very Weak |
| 28–35 bits | Weak |
| 36–59 bits | Fair |
| 60–127 bits | Strong |
| ≥ 128 bits | Very Strong |

## Project Structure

```
password-checker/
├── main.py           # Tkinter GUI
├── checker.py        # Strength analysis logic
├── generator.py      # Secure password generation
├── requirements.txt
└── README.md
```

## Setup & Run

```bash
git clone https://github.com/yourusername/password-checker
cd password-checker
pip install -r requirements.txt
python main.py
```

## Technologies

- Python 3.x
- Tkinter (GUI)
- `secrets` module (cryptographic randomness)
- `math`, `re`, `string` (standard library)

## What I Learned

- Entropy-based password scoring
- Difference between `random` and `secrets` modules in Python
- GUI development with Tkinter
- Regex-based pattern matching
- Cryptographically secure random generation

---
Built by Krovvidi Mani Kumar | B.Tech CSE (Cybersecurity & Blockchain)
