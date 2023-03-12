from fastapi import FastAPI, APIRouter
from pocketguardapp.settings.settings import PORT
import uvicorn


# app imports
from pocketguardapp.account import account_router


app = FastAPI()
v1 = APIRouter(prefix="/v1")

# router inclusion
v1.include_router(account_router)

# app inclusion
app.include_router(v1)

@app.get("/")
async def root():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
