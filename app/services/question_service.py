from uuid import UUID
from app.models.question import Question, QuestionCreate
from app.repositories.question_repository import QuestionRepository
import logging

logger = logging.getLogger("question-service.service")

class QuestionService:
    def __init__(self, repository: QuestionRepository):
        self.repository = repository

    def get_question(self, id: UUID) -> Question | None:
        return self.repository.get_by_id(id)

    def create_question(self, question: QuestionCreate) -> Question:
        logger.info("Сервис: создание вопроса")
        return self.repository.create(question)

    def answer_question(self, id: UUID, teacher_id: UUID, answer_text: str) -> Question:
        logger.info(f"Сервис: ответ на вопрос {id}")
        return self.repository.update_answer(id, teacher_id, answer_text)

    def close_question(self, id: UUID) -> Question:
        return self.repository.close_question(id)

