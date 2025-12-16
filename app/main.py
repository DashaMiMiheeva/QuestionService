import logging
from fastapi import FastAPI
from app.endpoints.question_router import question_router
from app.database import create_tables

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("question-service")

app = FastAPI(title="Question to Teacher Service", version="1.0.0")

@app.on_event("startup")
def on_startup():
    logger.info("Запуск сервиса 'Вопрос преподавателю'")
    create_tables()
    logger.info("Таблицы базы данных инициализированы")

app.include_router(question_router, prefix="/api")
