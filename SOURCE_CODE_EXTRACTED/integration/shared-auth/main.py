#!/usr/bin/env python3
"""
NEXUS Shared Auth v2.0.0 — RS256 JWT SSO
"""
import os
import time
import base64
import hashlib
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

app = FastAPI(title="NEXUS Auth", version="2.0.0-rs256")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────── Config ─────────────────────────────────────
ALGORITHM = "RS256"
KID = "nexus-key-1"
PRIVATE_KEY_PATH = os.getenv("JWT_PRIVATE_KEY_PATH", "/app/keys/private.pem")
PUBLIC_KEY_PATH = os.getenv("JWT_PUBLIC_KEY_PATH", "/app/keys/public.pem")
TOKEN_EXPIRY = int(os.getenv("JWT_TOKEN_EXPIRY", "86400"))

# Load keys
private_key = None
public_key = None


def load_keys():
    global private_key, public_key
    try:
        with open(PRIVATE_KEY_PATH, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )
        with open(PUBLIC_KEY_PATH, "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(), backend=default_backend()
            )
        print("[AUTH] ✅ RSA keys loaded")
    except Exception as e:
        print(f"[AUTH] ⚠️ Key loading failed: {e}")


load_keys()


# ─────────────────── Models ─────────────────────────────────────
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ─────────────────── Mock DB ────────────────────────────────────
USERS_DB = {
    "admin@mrf103.com": {
        "id": 1,
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin",
        "name": "MrF",
        "products": ["all"]
    },
    "user@mrf103.com": {
        "id": 2,
        "password_hash": hashlib.sha256("user123".encode()).hexdigest(),
        "role": "user",
        "name": "User",
        "products": ["alsultan-intelligence", "imperial-ui"]
    }
}


# ─────────────────── JWT Functions ──────────────────────────────
def create_access_token(data: dict, expires_delta: int = TOKEN_EXPIRY) -> str:
    if not private_key:
        raise HTTPException(500, "Private key not loaded")

    to_encode = data.copy()
    to_encode["exp"] = int(time.time()) + expires_delta
    to_encode["iat"] = int(time.time())

    return jwt.encode(
        to_encode,
        private_key,
        algorithm=ALGORITHM,
        headers={"kid": KID}
    )


def verify_access_token(token: str) -> dict:
    if not public_key:
        raise HTTPException(500, "Public key not loaded")

    return jwt.decode(token, public_key, algorithms=[ALGORITHM])


# ─────────────────── Endpoints ──────────────────────────────────
@app.get("/api/v1/auth/health")
def health():
    return {
        "status": "healthy",
        "service": "NEXUS Auth",
        "version": "2.0.0-rs256",
        "algorithm": ALGORITHM,
        "keys_loaded": private_key is not None and public_key is not None
    }


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = USERS_DB.get(request.email)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    password_hash = hashlib.sha256(request.password.encode()).hexdigest()
    if password_hash != user["password_hash"]:
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({
        "sub": str(user["id"]),
        "email": request.email,
        "role": user["role"],
        "name": user["name"]
    })

    return TokenResponse(access_token=token, expires_in=TOKEN_EXPIRY)


@app.get("/api/v1/auth/verify")
def verify_token(token: str):
    try:
        payload = verify_access_token(token)
        return {"valid": True, "user": payload.get("email"), "role": payload.get("role")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(401, f"Invalid token: {e}")


@app.get("/api/v1/auth/.well-known/jwks.json")
def get_jwks():
    """JWKS endpoint — any service can verify tokens with public key"""
    if not public_key:
        raise HTTPException(500, "Public key not loaded")

    pub_numbers = public_key.public_numbers()

    def int_to_base64url(num: int) -> str:
        byte_len = (num.bit_length() + 7) // 8
        return base64.urlsafe_b64encode(
            num.to_bytes(byte_len, byteorder='big')
        ).decode('utf-8').rstrip('=')

    return {
        "keys": [{
            "kty": "RSA",
            "kid": KID,
            "use": "sig",
            "alg": ALGORITHM,
            "n": int_to_base64url(pub_numbers.n),
            "e": int_to_base64url(pub_numbers.e)
        }]
    }


if __name__ == "__main__":
    import uvicorn
    print("🔐 Starting NEXUS Auth (RS256) on http://localhost:8002")
    uvicorn.run(app, host="0.0.0.0", port=8002)
