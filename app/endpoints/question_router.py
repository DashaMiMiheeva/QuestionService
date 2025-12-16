from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.models.question import Question, QuestionCreate
from app.services.question_service import QuestionService
from app.repositories.question_repository import QuestionRepository
from app.database import get_db
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger("question-service.router")
question_router = APIRouter(prefix="/questions", tags=["Questions"])

def get_question_service(db: Session = Depends(get_db)) -> QuestionService:
    repository = QuestionRepository(db)
    return QuestionService(repository)

@question_router.post("/", response_model=Question)
def create_question(
    question: QuestionCreate,
    service: QuestionService = Depends(get_question_service)
):
    logger.info( f"POST /questions | Создание вопроса | student_id={question.student_id}")
    result = service.create_question(question)
    logger.info(f"Вопрос успешно создан | question_id={result.id}")
    return result

@question_router.post("/{question_id}/answer", response_model=Question)
def answer_question(
    question_id: UUID,
    teacher_id: UUID,
    answer_text: str,
    service: QuestionService = Depends(get_question_service)
):
    logger.info( f"POST /questions/{question_id}/answer | teacher_id={teacher_id}")
    try:
        result = service.answer_question(question_id, teacher_id, answer_text)
        logger.info(f"Вопрос {question_id} успешно отвечен")
        return result
    except ValueError as e:
        logger.warning( f"Ошибка ответа на вопрос {question_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@question_router.post("/{question_id}/close", response_model=Question)
def close_question(
    question_id: UUID,
    service: QuestionService = Depends(get_question_service)
):
    logger.info(f"POST /questions/{question_id}/close")
    try:
        result = service.close_question(question_id)
        logger.info(f"Вопрос {question_id} успешно закрыт")
        return result
    except ValueError as e:
        logger.warning( f"Ошибка закрытия вопроса {question_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))