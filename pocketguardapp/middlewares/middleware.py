from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pocketguardapp.services.account import get_account, decode_token

app = APIRouter()


@app.middleware(
    "http",
    "https",
)
def authenticate(request: Request, call_next):
    token = request.headers.get("Authorization")

    if not token:
        return JSONResponse(status_code=401, content={"detail": "token not found"})

    # get email from token
    email = decode_token(token)["email"]
    account, error = get_account(email)

    if error:
        return JSONResponse(status_code=error.code, content={"detail": error.msg})

    request.state.account = account
    response = call_next(request)
    return response
