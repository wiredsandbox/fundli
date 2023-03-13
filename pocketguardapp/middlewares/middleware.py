from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pocketguardapp.services.account import get_account, decode_token

app = APIRouter()


@app.middleware(
    "http",
    "https",
)
def authenticate(request: Request, call_next):
    token = get_authorization_token(request)
    if not token:
        return JSONResponse(status_code=401, content={"detail": "token not found"})

    # get email from token
    email = decode_token(token).get("email")
    account, error = get_account(email)

    if error:
        return JSONResponse(status_code=error.code, content={"detail": error.msg})

    request.state.account = account
    return call_next(request)


def get_authorization_token(request: Request):
    """
    get_authorization_token returns the authorization token from the request
    expects format: Authorization: Bearer <token>
    """
    parts = str(request.headers.get("Authorization")).split(" ")
    if len(parts) != 2:
        return None
    return parts[1]

