#!/usr/bin/env python3
"""
Generate RS256 keypair for NEXUS Auth (nexus_auth).
Output: private.pem, public.pem in KEYS_DIR (default: ./data/auth_keys).
Run before starting nexus_auth: KEYS_DIR=/path python generate_keys.py
"""

import os
import sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("ERROR: Install cryptography: pip install cryptography", file=sys.stderr)
    sys.exit(1)

KEYS_DIR = os.environ.get("KEYS_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "data", "auth_keys"))
KEY_SIZE = 2048


def main():
    keys_path = Path(KEYS_DIR)
    keys_path.mkdir(parents=True, exist_ok=True)

    private_path = keys_path / "private.pem"
    public_path = keys_path / "public.pem"

    if private_path.exists() and public_path.exists():
        print(f"[generate_keys] Keys already exist in {keys_path}. Skipping.")
        return 0

    print(f"[generate_keys] Generating RS256 keypair in {keys_path}...")
    key = rsa.generate_private_key(public_exponent=65537, key_size=KEY_SIZE, backend=default_backend())

    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    private_path.write_bytes(private_pem)
    public_path.write_bytes(public_pem)
    os.chmod(private_path, 0o600)
    os.chmod(public_path, 0o644)

    print(f"[generate_keys] Created: {private_path}, {public_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
