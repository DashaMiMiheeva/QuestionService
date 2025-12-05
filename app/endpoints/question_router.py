from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.models.question import Question, QuestionCreate
from app.services.question_service import QuestionService
from app.repositories.question_repository import QuestionRepository
from app.database import get_db
from sqlalchemy.orm import Session

question_router = APIRouter(prefix="/questions", tags=["Questions"])

def get_question_service(db: Session = Depends(get_db)) -> QuestionService:
    repository = QuestionRepository(db)
    return QuestionService(repository)

@question_router.post("/", response_model=Question)
def create_question(
    question: QuestionCreate,
    service: QuestionService = Depends(get_question_service)
):
    return service.create_question(question)

@question_router.post("/{question_id}/answer", response_model=Question)
def answer_question(
    question_id: UUID,
    teacher_id: UUID,
    answer_text: str,
    service: QuestionService = Depends(get_question_service)
):
    try:
        return service.answer_question(question_id, teacher_id, answer_text)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@question_router.post("/{question_id}/close", response_model=Question)
def close_question(
    question_id: UUID,
    service: QuestionService = Depends(get_question_service)
):
    try:
        return service.close_question(question_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))