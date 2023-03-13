from fastapi import APIRouter, HTTPException
from .schemas.account_schemas import (
    AccountRequest, 
    AccountResponse,
    AccountLoginRequest,
    )
from .services import account as account_service


account_router = APIRouter(prefix="/account")


@account_router.post("/signup", response_model=AccountResponse)
async def signup(request: AccountRequest):
    account, error = account_service.create_account(
        email=request.email,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name,
    )
    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not account:
        raise HTTPException(status_code=500, detail="failed to create account")

    token = account_service.generate_token(
        account.email, account.first_name, account.last_name
    )

    #  map account to account response
    account = account.to_dict()
    account_response = AccountResponse(
        id=account["_id"],
        email=account["email"],
        first_name=account["first_name"],
        last_name=account["last_name"],
        token=token,
    )
    return account_response


# @account_router.post("/login", response_model=AccountResponse)
# async def login(request: AccountLoginRequest):
