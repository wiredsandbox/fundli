from fastapi import APIRouter, HTTPException, Request 
from fastapi.responses import JSONResponse
from pocketguardapp.services.account import get_account

app = APIRouter()


# show me how to use get account in fastapi middleware
@app.middleware("http","https", )
def get_account_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse(status_code=401, content={"detail": "token not found"})

    account, error = get_account(token)
    if error:
        return JSONResponse(status_code=error.code, content={"detail": error.msg})

    request.state.account = account
    response = call_next(request)
    return response