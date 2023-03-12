from fastapi import APIRouter, HTTPException
from .schemas.account_schemas import AccountRequest
from .services import account as account_service


account_router = APIRouter(prefix="/account")


@account_router.post("/signup")
async def signup(request: AccountRequest):
    account, error = account_service.create_account(
        email=request.email,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name,
    )
    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)
