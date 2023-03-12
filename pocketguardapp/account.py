from fastapi import APIRouter
from .schemas.account_schemas import AccountRequest


account_router = APIRouter(prefix="/account")


@account_router.post("/signup")
async def signup(request: AccountRequest):

    return {"message": "signup"}
