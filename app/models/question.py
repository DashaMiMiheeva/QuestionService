import enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class QuestionStatus(enum.Enum):
    CREATED = "created"
    ANSWERED = "answered"
    CLOSED = "closed"


class QuestionBase(BaseModel):
    title: str
    content: str
    student_id: UUID
    teacher_id: UUID | None = None


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: QuestionStatus
    created_at: datetime
    answered_at: datetime | None = None
    closed_at: datetime | None = None
    answer_text: str | None = None