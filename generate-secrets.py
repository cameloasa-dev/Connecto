import secrets
import secrets

def generate_key():
    return secrets.token_hex(32)

print("🔐 Generating secure secrets...")

print(f"SECRET_KEY={generate_key()}")
print(f"SESSION_SECRET_KEY={generate_key()}")

print("\nCopy these values into backend/.env")
