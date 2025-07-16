import base64, hashlib, urllib.parse

def check_password(password: str, hashed: str) -> bool:
    parts = urllib.parse.unquote(hashed).split('$')
    if len(parts) != 3:
        return False
    iterations = int(parts[0])
    salt = base64.b64decode(parts[1])
    true_hash = base64.b64decode(parts[2])
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return new_hash == true_hash

print(check_password("plantify123", "100000$rekZVGwzssmgyD6M83OVag==$Z+pfzTjnc70ElEBqbGcAgOXFc6xRDOM/HaxwBhqEtjs="))