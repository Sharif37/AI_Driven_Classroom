from fastapi import FastAPI
from app.routes.upload import router as upload_router

app = FastAPI()

app.include_router(upload_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Document Chat API"}
