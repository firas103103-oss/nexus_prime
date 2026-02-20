"""
Authentication middleware
"""

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(token: str):
    """Verify JWT token"""
    # Placeholder - integrate with Supabase later
    if token == "test-token":
        return True
    return False

async def auth_middleware(request: Request, call_next):
    """Authentication middleware"""
    # Skip auth for health checks
    if request.url.path in ["/", "/api/v1/health"]:
        return await call_next(request)
    
    # Check authorization header
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization")
    
    token = auth.replace("Bearer ", "")
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return await call_next(request)
