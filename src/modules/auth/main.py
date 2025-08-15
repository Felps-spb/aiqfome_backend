from fastapi import FastAPI
from dotenv import load_dotenv
from src.modules.auth.http.rest.controller.auth_controller import router as auth_router

load_dotenv()
app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
