from fastapi import APIRouter, HTTPException, Depends
from .schemas.account_schemas import (
    AccountRequest,
    AccountLoginRequest,
    AccountAuthResponse,
    AccountResponse,
    account_auth_response_serializer,
    account_response_serializer,
)
from .services import account as account_service
from .models.account_models import Account
from .middlewares.middleware import authenticate


account_router = APIRouter(prefix="/account")


@account_router.post("/signup", response_model=AccountAuthResponse)
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

    return account_auth_response_serializer(account, token)


@account_router.post("/login", response_model=AccountAuthResponse)
async def login(request: AccountLoginRequest):
    account, error = account_service.login_account(
        email=request.email, password=request.password
    )
    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not account:
        raise HTTPException(status_code=500, detail="failed to login account")

    token = account_service.generate_token(
        account.email, account.first_name, account.last_name
    )

    return account_auth_response_serializer(account, token)


@account_router.get("/me", response_model=AccountResponse)
async def get_me(activeAccount: Account = Depends(authenticate)):
    """
    get_me returns the account for the authenticated user
    """
    return account_response_serializer(activeAccount)
