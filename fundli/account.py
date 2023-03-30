from fastapi import APIRouter, Depends, HTTPException

from fundli.email_service.email_schema import EmailResponse

from .middlewares.middleware import authenticate
from .models.account_models import Account
from .schemas.account_schemas import (
    AccountAuthResponse,
    AccountLoginRequest,
    AccountRequest,
    AccountResponse,
    account_auth_response_serializer,
    account_response_serializer,
)
from .services import account as account_service

account_router = APIRouter(prefix="/account")


@account_router.post("/signup", response_model=AccountAuthResponse)
async def signup(request: AccountRequest):
    """
    intro-->

            This endpoint is used to create a new account. It takes in a request body with the following fields:

    paramDesc-->

            reqBody-->email-->The email of the account
            reqBody-->password-->The password of the account
            reqBody-->first_name-->The first name of the account
            reqBody-->last_name-->The last name of the account

    returnDesc-->

            On success, the endpoint returns an AccountAuthResponse object with the following fields:

    paramDesc-->

            id-->The id of the account
            email-->The email of the account
            first_name-->The first name of the account
            last_name-->The last name of the account
            token-->The JWT token for the account

    returnDesc-->

            On failure, the endpoint returns an error with the following fields:

    paramDesc-->

            code-->The HTTP status code of the error
            msg-->The error message

            example-->

                error code: 400
                message:{
                    "detail": "email already exists"
                    }
    """
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
    """intro-->

        This endpoint is used to login an account. It takes in a request body with the following fields:

    paramDesc-->

            reqBody-->email-->The email of the account
            reqBody-->password-->The password of the account

    returnDesc-->

            On success, the endpoint returns an AccountAuthResponse object with the following fields:

    paramDesc-->

            id-->The id of the account
            email-->The email of the account
            first_name-->The first name of the account
            last_name-->The last name of the account
            token-->The JWT token for the account

    returnDesc-->

            On failure, the endpoint returns an error with the following fields:

    paramDesc-->

            code-->The HTTP status code of the error
            msg-->The error message

            example-->

                error code: 500
                message:{
                    "detail": "failed to login account"
                    }
    """
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
    intro-->

        This endpoint is used to get the account of the currently logged in user. It takes in a request body with the following fields:

    paramDesc-->

            reqBody-->Header-->Authorization-->The JWT token of the account

    returnDesc-->

            On success, the endpoint returns an AccountResponse object with the following fields:

    paramDesc-->

            id-->The id of the account
            email-->The email of the account
            first_name-->The first name of the account
            last_name-->The last name of the account

    returnDesc-->

            On failure, the endpoint returns an error with the following fields:

    paramDesc-->

            code-->The HTTP status code of the error
            msg-->The error message

            example-->

                error code: 401
                message:{
                    "detail": "token not found"
                    }
    """
    return account_response_serializer(activeAccount)


@account_router.get("/forgot-password", response_model=EmailResponse)
async def forgot_password(email: str):
    """
    intro-->

        This endpoint is used to send a password reset email to the account with the specified email. It takes in a request body with the following fields:

    paramDesc-->

            reqBody-->email-->The email of the account

    returnDesc-->

            On success, the endpoint returns a success message with the following fields:

    paramDesc-->

            msg-->The success message

            example-->

                message:{
                    "msg": "password reset email sent"
                    }
    """
    forgot_password_email, error = account_service.forgot_password(
        email, code=account_service.generate_verification_code(6)
    )
    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    return forgot_password_email


@account_router.get(
    "/reset-password{email}/{code}/{password}", response_model=EmailResponse
)
async def reset_password(email: str, code: int, password: str):
    """
    intro-->

        This endpoint is used to reset the password of the account with the specified email. It takes in a request body with the following fields:

    paramDesc-->

            reqBody-->email-->The email of the account
            reqBody-->code-->The verification code sent to the account
            reqBody-->password-->The new password of the account

    returnDesc-->

            On success, the endpoint returns a success message with the following fields:

    paramDesc-->

            msg-->The success message

            example-->

                message:{
                    "msg": "password reset successful"
                    }
    """
    _, error = account_service.reset_password(email, password, code)
    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    return EmailResponse(message="password reset successful")
