import base64
import os
from typing import Callable, Awaitable
from fastapi import Request, Response

USERNAME = os.getenv("DEMO_USERNAME", "")
PASSWORD = os.getenv("DEMO_PASSWORD", "")

# call_next is a function that takes a Request and returns an Awaitable[Response]
CallNext = Callable[[Request], Awaitable[Response]]

async def basic_auth(request: Request, call_next: CallNext) -> Response:
    auth = request.headers.get("Authorization")
    if auth:
        try:
            scheme, credentials = auth.split()
            if scheme.lower() == "basic":
                decoded = base64.b64decode(credentials).decode("utf-8")
                user, pwd = decoded.split(":", 1)
                if user == USERNAME and pwd == PASSWORD:
                    return await call_next(request)
        except Exception:
            pass

    return Response(
        status_code=401,
        headers={"WWW-Authenticate": "Basic realm='slotplanner-demo'"}
    )
