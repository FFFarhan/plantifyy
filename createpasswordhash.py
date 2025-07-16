import os, base64, hashlib, urllib.parse

def hash_password(password: str, iterations: int = 100_000) -> str:
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    salt_b64 = base64.b64encode(salt).decode()
    hash_b64 = base64.b64encode(hash_bytes).decode()
    password_hash = f"{iterations}${salt_b64}${hash_b64}"
    return urllib.parse.quote(password_hash, safe='')

print(hash_password("plantify123"))