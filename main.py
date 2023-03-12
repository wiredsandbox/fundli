import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter

from pocketguardapp.settings.settings import PORT
from pocketguardapp.account import account_router


v1 = APIRouter(prefix="/v1")
v1.include_router(account_router)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1)


@app.get("/")
async def root():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=PORT, reload=True)
