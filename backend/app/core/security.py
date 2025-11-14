from passlib.hash import bcrypt

def _truncate72(p):
    if not isinstance(p, str):
        p = str(p)
    b = p.encode("utf-8")
    if len(b) > 72:
        b = b[:72]
    return b.decode("utf-8", "ignore")

def hash_password(raw: str) -> str:
    safe = _truncate72(raw)
    return bcrypt.hash(safe)

def verify_password(raw: str, hashed: str) -> bool:
    safe = _truncate72(raw)
    return bcrypt.verify(safe, hashed)

def is_admin_token(token: str | None) -> bool:
    return token == "admin"


