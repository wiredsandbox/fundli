import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from fundli.account import account_router
from fundli.settings.settings import PORT, TEMPLATE_FOLDER
from fundli.transaction import transaction_router

v1 = APIRouter(prefix="/v1")
v1.include_router(account_router, tags=["Account"])
v1.include_router(transaction_router, tags=["Transaction"])

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


@app.get("/files/logo")
async def get_file():
    return FileResponse(TEMPLATE_FOLDER + "/email/images/logo.svg")


if __name__ == "__main__":
    # start app
    uvicorn.run("main:app", port=PORT, reload=True)
