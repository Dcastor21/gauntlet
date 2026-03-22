from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
import httpx

from app.config import get_settings

security = HTTPBearer()
_jwks_cache: dict | None = None


async def _get_jwks() -> dict:
    """Fetch and cache Clerk's JWKS for JWT verification."""
    global _jwks_cache
    if _jwks_cache is None:
        settings = get_settings()
        async with httpx.AsyncClient() as client:
            resp = await client.get(settings.clerk_jwks_url)
            resp.raise_for_status()
            _jwks_cache = resp.json()
    return _jwks_cache


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> dict:
    """
    Validate Clerk JWT and return user claims.

    Returns dict with at minimum: {"user_id": "user_xxx", ...}
    Raises 401 if token is invalid or expired.
    """
    token = credentials.credentials
    try:
        jwks = await _get_jwks()
        # Clerk uses RS256 — get the signing key from JWKS
        unverified_header = jwt.get_unverified_header(token)
        key = None
        for k in jwks.get("keys", []):
            if k["kid"] == unverified_header.get("kid"):
                key = k
                break

        if key is None:
            raise HTTPException(status_code=401, detail="Invalid token signing key")

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            options={"verify_aud": False},  # Clerk doesn't always set aud
        )
        return {
            "user_id": payload.get("sub", ""),
            "email": payload.get("email", ""),
            "metadata": payload.get("public_metadata", {}),
        }
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {e}")