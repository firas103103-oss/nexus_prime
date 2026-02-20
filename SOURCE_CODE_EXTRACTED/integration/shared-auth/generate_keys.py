#!/usr/bin/env python3
"""RSA Key Generator for RS256 JWT"""
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEYS_DIR = os.getenv("KEYS_DIR", "/app/keys")


def generate():
    os.makedirs(KEYS_DIR, exist_ok=True)
    priv_path = f"{KEYS_DIR}/private.pem"
    pub_path = f"{KEYS_DIR}/public.pem"

    if os.path.exists(priv_path) and os.path.exists(pub_path):
        print(f"[AUTH] Keys already exist at {KEYS_DIR}")
        return

    print(f"[AUTH] Generating RSA-2048 keypair...")
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    with open(priv_path, "wb") as f:
        f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        ))

    with open(pub_path, "wb") as f:
        f.write(key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print(f"[AUTH] ✅ Keys generated: {priv_path}, {pub_path}")


if __name__ == "__main__":
    generate()
