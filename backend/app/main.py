from fastapi import FastAPI
from app.routers.user import router as user_router

app = FastAPI()

app.include_router(user_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Sport API backend is running 🚀"}