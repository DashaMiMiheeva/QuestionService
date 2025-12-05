from sqlalchemy import Column, String, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.base_schema import Base
from app.models.question import QuestionStatus

class QuestionDB(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    student_id = Column(UUID(as_uuid=True), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(Enum(QuestionStatus), default=QuestionStatus.CREATED)
    created_at = Column(DateTime, nullable=False)
    answered_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    answer_text = Column(Text, nullable=True)