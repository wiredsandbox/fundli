from fastapi import FastAPI


from pocketguardapp.settings.settings import PORT
import uvicorn

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}








if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port = PORT, reload = True)