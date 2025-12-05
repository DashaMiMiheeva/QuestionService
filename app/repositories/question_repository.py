from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.question import Question, QuestionStatus, QuestionCreate
from app.schemas.question import QuestionDB


class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: UUID) -> Question | None:
        question = self.db.query(QuestionDB).filter(QuestionDB.id == id).first()
        return Question.model_validate(question) if question else None

    def create(self, question: QuestionCreate) -> Question:
        db_question = QuestionDB(
            id=uuid4(),
            title=question.title,
            content=question.content,
            student_id=question.student_id,
            status=QuestionStatus.CREATED,
            created_at=datetime.now()
        )
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return Question.model_validate(db_question)

    def update_answer(self, id: UUID, teacher_id: UUID, answer_text: str) -> Question:
        question = self.db.query(QuestionDB).filter(QuestionDB.id == id).first()
        if not question:
            raise ValueError("Question not found")

        question.teacher_id = teacher_id
        question.answer_text = answer_text
        question.status = QuestionStatus.ANSWERED
        question.answered_at = datetime.now()

        self.db.commit()
        self.db.refresh(question)
        return Question.model_validate(question)

    def close_question(self, id: UUID) -> Question:
        question = self.db.query(QuestionDB).filter(QuestionDB.id == id).first()
        if not question:
            raise ValueError("Question not found")

        question.status = QuestionStatus.CLOSED
        question.closed_at = datetime.now()

        self.db.commit()
        self.db.refresh(question)
        return Question.model_validate(question)