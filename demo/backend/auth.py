import base64
import os
from typing import Callable, Awaitable
from fastapi import Request, Response, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from jose import jwt

DEMO_USERNAME = os.getenv("DEMO_USERNAME")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD")

# call_next is a function that takes a Request and returns an Awaitable[Response]
CallNext = Callable[[Request], Awaitable[Response]]


# Basic Auth = human users accessing HTML admin pages
# Managed Identity = Azure Functions calling backend automation endpoints


# ------------------------------------------------------------
# Basic Auth Middleware for Protecting Demo Pages
# ------------------------------------------------------------

ALLOWED_BEARER_PATHS = {
    "/demo/admin/generate_next_week",
    "/demo/admin/cleanup_old"
}

async def basic_auth(request: Request, call_next: CallNext) -> Response:
    auth = request.headers.get("Authorization")
    if auth:
        try:
            scheme, credentials = auth.split()

            #Allow Bearer tokens ONLY for designated automation endpoints
            if scheme.lower() == "bearer":
                if request.url.path in ALLOWED_BEARER_PATHS:
                    return await call_next(request)
                else:
                    return Response(
                        status_code=401,
                        headers={"WWW-Authenticate": "Basic realm='slotplanner-demo'"}
                    )

            if scheme.lower() == "basic":
                decoded = base64.b64decode(credentials).decode("utf-8")
                user, pwd = decoded.split(":", 1)
                if user == DEMO_USERNAME and pwd == DEMO_PASSWORD:
                    return await call_next(request)
        except Exception:
            pass

    return Response(
        status_code=401,
        headers={"WWW-Authenticate": "Basic realm='slotplanner-demo'"}
    )


# ------------------------------------------------------------
# Managed Identity Token Validation (Azure AD)
# ------------------------------------------------------------

TENANT_ID = "de3de62f-be92-4aa5-a184-3039941d9215"
FUNCTION_MI_OBJECT_ID = "e122f580-1216-4f66-a735-dbf334dbc1b5"
AUDIENCE = "api://7354ba0f-dab1-4a16-b16d-2864021087d4"

jwks_cache = None
bearer_scheme = HTTPBearer(auto_error=True)


async def get_jwks():
    global jwks_cache
    if jwks_cache is None:
        url = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            jwks_cache = resp.json()
    return jwks_cache


async def validate_managed_identity(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials

    jwks = await get_jwks()

    try:
        # Validate signature + issuer + audience
        claims = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=f"https://sts.windows.net/{TENANT_ID}/"
        )

        # Validate that the token belongs to your Function App MI
        if claims.get("oid") != FUNCTION_MI_OBJECT_ID:
            raise HTTPException(status_code=401, detail="Invalid Managed Identity")

        return claims

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")