# run_ci_tests.py в корне проекта
#!/usr/bin/env python3
"""
Запуск тестов в CI окружении
"""
import sys
import os
import subprocess

# Устанавливаем абсолютный путь
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"Запуск из: {current_dir}")
print(f"Содержимое app/: {os.listdir('app') if os.path.exists('app') else 'app не существует'}")

# Запускаем pytest
result = subprocess.run([
    sys.executable, "-m", "pytest",
    "tests/unit/test_question.py",
    "-v",
    "--tb=short"
], cwd=current_dir)

sys.exit(result.returncode)