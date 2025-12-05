import pytest
import requests
import time
from uuid import uuid4
import subprocess
import sys
from typing import Generator
import os

BASE_URL = "http://localhost:8000/api/questions"


@pytest.fixture(scope="session")
def start_server() -> Generator[None, None, None]:
    for _ in range(3):
        try:
            response = requests.get("http://localhost:8000/docs", timeout=2)
            if response.status_code == 200:
                print("Сервер уже запущен")
                yield
                return
        except:
            time.sleep(1)

    server_process = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "DATABASE_URL": "sqlite:///./test.db"}
    )

    print("Ожидаем запуск сервера...")
    for attempt in range(10):
        try:
            response = requests.get("http://localhost:8000/docs", timeout=2)
            if response.status_code == 200:
                print(f"Сервер запущен за {attempt + 1} секунд")
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        server_process.terminate()
        pytest.fail("Не удалось запустить сервер за 10 секунд")

    yield

    print("Останавливаем сервер...")
    server_process.terminate()
    server_process.wait()


@pytest.fixture
def unique_student_id() -> str:
    return str(uuid4())

@pytest.fixture
def sample_question_data(unique_student_id: str) -> dict:
    return {
        "title": "Тест",
        "content": "Текст теста",
        "student_id": unique_student_id
    }


class TestQuestionAPICreate:
    def test_create_question_success(self, start_server: None, sample_question_data: dict):
        response = requests.post(BASE_URL, json=sample_question_data)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"

        data = response.json()

        assert "id" in data, "Ответ должен содержать поле 'id'"
        assert data["title"] == sample_question_data["title"]
        assert data["content"] == sample_question_data["content"]
        assert data["student_id"] == sample_question_data["student_id"]

        assert data["status"] == "created", f"Статус должен быть 'created', а не '{data['status']}'"
        assert data["teacher_id"] is None, "teacher_id должен быть null при создании"
        assert data["answer_text"] is None, "answer_text должен быть null при создании"
        assert data["created_at"] is not None, "created_at должен быть установлен"

        print(f"Создан вопрос с ID: {data['id']}")
        return data["id"]

    def test_create_question_validation_error(self, start_server: None):
        invalid_data = {
            "title": "",
            "content": "Содержание",
            "student_id": str(uuid4())
        }

        response = requests.post(BASE_URL, json=invalid_data)
        assert response.status_code == 422, "Пустой заголовок должен вызывать 422"

        missing_fields = {
            "title": "Только заголовок"
        }

        response = requests.post(BASE_URL, json=missing_fields)
        assert response.status_code == 422, "Отсутствие обязательных полей должно вызывать 422"

class TestQuestionAPIAnswer:
    def create_test_question(self, student_id: str = None) -> str:
        if student_id is None:
            student_id = str(uuid4())

        question_data = {
            "title": "Вопрос для ответа",
            "content": "Содержание вопроса",
            "student_id": student_id
        }

        response = requests.post(BASE_URL, json=question_data)
        return response.json()["id"]

    def test_answer_question_success(self, start_server: None):
        question_id = self.create_test_question()
        teacher_id = str(uuid4())
        answer_text = "Ответ на тестовый запрос"

        response = requests.post(
            f"{BASE_URL}/{question_id}/answer",
            params={
                "teacher_id": teacher_id,
                "answer_text": answer_text
            }
        )

        assert response.status_code == 200, f"Ошибка: {response.text}"
        data = response.json()

        assert data["status"] == "answered", f"Статус должен быть 'answered', а не '{data['status']}'"
        assert data["teacher_id"] == teacher_id, "teacher_id должен сохраниться"
        assert data["answer_text"] == answer_text, "Текст ответа должен сохраниться"
        assert data["answered_at"] is not None, "answered_at должен быть установлен"

        print(f"Ответ на вопрос {question_id} успешно добавлен")

    def test_answer_nonexistent_question(self, start_server: None):
        non_existent_id = str(uuid4())
        teacher_id = str(uuid4())

        response = requests.post(
            f"{BASE_URL}/{non_existent_id}/answer",
            params={
                "teacher_id": teacher_id,
                "answer_text": "Ответ"
            }
        )

        assert response.status_code == 404, "Несуществующий вопрос должен возвращать 404"

        error_data = response.json()
        assert "detail" in error_data, "Ответ об ошибке должен содержать поле 'detail'"
        assert "not found" in error_data["detail"].lower()

        print("404 ошибка для несуществующего вопроса работает корректно")


class TestQuestionAPIClose:
    def create_answered_question(self) -> str:
        student_id = str(uuid4())
        question_data = {
            "title": "Вопрос для закрытия",
            "content": "Этот вопрос будет закрыт",
            "student_id": student_id
        }

        response = requests.post(BASE_URL, json=question_data)
        question_id = response.json()["id"]

        teacher_id = str(uuid4())
        requests.post(
            f"{BASE_URL}/{question_id}/answer",
            params={
                "teacher_id": teacher_id,
                "answer_text": "Ответ перед закрытием"
            }
        )

        return question_id

    def test_close_question_success(self, start_server: None):
        question_id = self.create_answered_question()

        response = requests.post(f"{BASE_URL}/{question_id}/close")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "closed", f"Статус должен быть 'closed', а не '{data['status']}'"
        assert data["closed_at"] is not None, "closed_at должен быть установлен"

        print(f"Вопрос {question_id} успешно закрыт")


if __name__ == "__main__":
    """
    Запуск тестов напрямую: python tests/e2e/test_question_api.py
    Убедитесь, что сервер запущен на localhost:8000
    """
    print("Для запуска E2E тестов используйте: pytest tests/e2e/test_question_api.py -v")