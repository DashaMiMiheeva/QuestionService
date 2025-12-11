import pytest
from uuid import uuid4, UUID
from datetime import datetime
from unittest.mock import Mock
from app.models.question import Question, QuestionStatus, QuestionCreate
from app.services.question_service import QuestionService

class TestQuestionModels:
    def test_create_question_with_valid_data(self):
        question = QuestionCreate(title="Test title", content="Test content", student_id=uuid4())
        assert question.title == "Test title"
    def test_question_status_values(self):
        assert QuestionStatus.CREATED.value == "created"
        assert QuestionStatus.ANSWERED.value == "answered"
        assert QuestionStatus.CLOSED.value == "closed"

class TestQuestionService:
    @pytest.fixture
    def mock_repo(self): return Mock()

    @pytest.fixture
    def service(self, mock_repo): return QuestionService(mock_repo)

    @pytest.fixture
    def sample_question(self):
        return Question(
            id=uuid4(),
            title="Тестовый вопрос",
            content="Содержание тестового вопроса",
            student_id=uuid4(),
            teacher_id=None,
            status=QuestionStatus.CREATED,
            created_at=datetime.now(),
            answered_at=None,
            closed_at=None,
            answer_text=None
        )
    def test_service_creates_question(self, service, mock_repo):
        student_id = uuid4()
        question_data = QuestionCreate(
            title="Вопрос по тестированию",
            content="Как писать тесты для FastAPI?",
            student_id=student_id)
        expected_question = Question(
            id=uuid4(),
            title=question_data.title,
            content=question_data.content,
            student_id=student_id,
            status=QuestionStatus.CREATED,
            created_at=datetime.now())
        mock_repo.create.return_value = expected_question
        result = service.create_question(question_data)
        assert result.title == question_data.title
        assert result.status == QuestionStatus.CREATED
        mock_repo.create.assert_called_once_with(question_data)
    def test_service_answers_question(self, service, mock_repo, sample_question):
        answered_question = Question(
            **{**sample_question.model_dump(),
               "status": QuestionStatus.ANSWERED,
               "teacher_id": uuid4(),
               "answer_text": "Ответ",
               "answered_at": datetime.now()})
        mock_repo.update_answer.return_value = answered_question
        result = service.answer_question(
            id=uuid4(),
            teacher_id=uuid4(),
            answer_text="Ответ от преподавателя")
        assert result.status == QuestionStatus.ANSWERED
        assert result.answer_text == "Ответ от преподавателя"
        mock_repo.update_answer.assert_called_once()
    def test_service_closes_question(self, service, mock_repo, sample_question):
        answered_question = Question(
            **{**sample_question.model_dump(),
               "status": QuestionStatus.ANSWERED,
               "teacher_id": uuid4(),
               "answer_text": "Ответ",
               "answered_at": datetime.now()})
        closed_question = Question( **{**answered_question.model_dump(), "status": QuestionStatus.CLOSED, "closed_at": datetime.now()})
        mock_repo.close_question.return_value = closed_question
        result = service.close_question(sample_question.id)
        assert result.status == QuestionStatus.CLOSED
        assert result.closed_at is not None
        mock_repo.close_question.assert_called_once()
