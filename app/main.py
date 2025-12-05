from fastapi import FastAPI
from app.endpoints.question_router import question_router
from app.database import create_tables

app = FastAPI(title="Question to Teacher Service", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(question_router, prefix="/api")