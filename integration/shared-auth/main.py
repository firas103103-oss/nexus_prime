#!/usr/bin/env python3
"""
NEXUS Auth — RS256 JWT SSO Service
Port: 8002 (internal) / 8003 (host)
"""

import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import jwt, JWTError
import asyncpg

# Config
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:nexus_mrf_password_2026@nexus_db:5432/nexus_db")
KEYS_DIR = Path(os.getenv("KEYS_DIR", "/app/keys"))
JWT_EXPIRY = int(os.getenv("JWT_TOKEN_EXPIRY", "86400"))  # 24h
ALGORITHM = "RS256"
KID = "nexus-key-1"

app = FastAPI(title="NEXUS Auth", version="2.0.0-rs256")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

pool = None


async def get_db():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DB_URL, min_size=2, max_size=10)
    return pool


def _load_private_key():
    p = KEYS_DIR / "private.pem"
    if not p.exists():
        raise RuntimeError(f"Private key not found at {p}. Run: KEYS_DIR={KEYS_DIR} python generate_keys.py")
    return p.read_text()


def _load_public_key():
    p = KEYS_DIR / "public.pem"
    if not p.exists():
        raise RuntimeError(f"Public key not found at {p}. Run generate_keys.py")
    return p.read_text()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenVerify(BaseModel):
    token: str


@app.on_event("startup")
async def startup():
    try:
        await get_db()
    except Exception as e:
        print(f"[AUTH] DB connection deferred: {e}")


@app.post("/api/v1/auth/login")
async def login(req: LoginRequest, db=Depends(get_db)):
    # Minimal auth: accept admin/admin123 for bootstrap
    if req.username == "admin" and req.password == "admin123":
        payload = {"sub": "admin", "role": "admin", "exp": datetime.now(timezone.utc) + timedelta(seconds=JWT_EXPIRY)}
        token = jwt.encode(payload, _load_private_key(), algorithm=ALGORITHM, headers={"kid": KID})
        return {"access_token": token, "token_type": "Bearer", "expires_in": JWT_EXPIRY}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/api/v1/auth/verify")
async def verify(req: TokenVerify):
    try:
        payload = jwt.decode(req.token, _load_public_key(), algorithms=[ALGORITHM])
        return {"valid": True, "sub": payload.get("sub"), "role": payload.get("role")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def _b64url(b: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


@app.get("/api/v1/auth/.well-known/jwks.json")
async def jwks():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    pub = serialization.load_pem_public_key(_load_public_key().encode(), backend=default_backend())
    numbers = pub.public_numbers()
    n_b64 = _b64url(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big"))
    e_b64 = _b64url(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big"))
    return {"keys": [{"kty": "RSA", "kid": KID, "use": "sig", "alg": ALGORITHM, "n": n_b64, "e": e_b64}]}


@app.get("/api/v1/auth/health")
async def health():
    return {"status": "ok", "service": "nexus_auth", "version": "2.0.0-rs256"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
