import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from settings import NON200_FILE, CANONICAL_FILE
from .utils import fetch, extract_canonical, _norm

# Списки для записи ошибок
_NON200_LINKS = []
_CANONICAL_MISMATCHES = []

# Тест: все ссылки должны возвращать статус 200
def test_status_200(urls):
    for url in urls:
        status_code, _ = fetch(url, head=True)
        if status_code != 200:
            _NON200_LINKS.append((url, status_code))

            # Записываем ошибки в файл
            with open(NON200_FILE, "w", encoding="utf-8") as file:
                for item in _NON200_LINKS:
                    link = item[0]
                    code = item[1]
                    file.write(f"{link} - {code}\n")

            assert status_code == 200, f"{url} → {status_code}"

# Тест: хотя бы одна ссылка должна быть с ошибкой (демо)
def test_status_not_200(urls):
    errors_found = False

    for url in urls:
        status_code, _ = fetch(url, head=True)
        if status_code != 200:
            errors_found = True
            _NON200_LINKS.append((url, status_code))

            with open(NON200_FILE, "w", encoding="utf-8") as file:
                for item in _NON200_LINKS:
                    link = item[0]
                    code = item[1]
                    file.write(f"{link} - {code}\n")

    assert errors_found, "Ожидалась хотя бы одна ссылка с ошибочным статусом"

# Тест: проверка совпадения canonical и URL
def test_canonical(urls):
    for url in urls:
        status_code, page_body = fetch(url)
        if status_code != 200:
            continue

        canonical_url = extract_canonical(page_body)

        if canonical_url is None:
            _CANONICAL_MISMATCHES.append((url, "NO CANONICAL"))

            with open(CANONICAL_FILE, "w", encoding="utf-8") as file:
                for item in _CANONICAL_MISMATCHES:
                    link = item[0]
                    canonical = item[1]
                    file.write(f"{link} - {canonical}\n")

            assert False, f"Отсутствует тег canonical на {url}"

        elif _norm(canonical_url) != _norm(url):
            _CANONICAL_MISMATCHES.append((url, canonical_url))

            with open(CANONICAL_FILE, "w", encoding="utf-8") as file:
                for item in _CANONICAL_MISMATCHES:
                    link = item[0]
                    canonical = item[1]
                    file.write(f"{link} - {canonical}\n")

            assert False, f"Несовпадение canonical на {url}: {canonical_url}"
