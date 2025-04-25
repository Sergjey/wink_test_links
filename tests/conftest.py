import pytest
from .utils import load_sitemap
from settings import NON200_FILE, CANONICAL_FILE
from .test_sitemap import _NON200_LINKS, _CANONICAL_MISMATCHES

# Загружаем ссылки из sitemap и custom_urls
@pytest.fixture(scope="session")
def urls():
    return load_sitemap()

# Хук — вызывается в самом конце pytest-сессии
def pytest_sessionfinish(session, *_):
    if _NON200_LINKS:
        with open(NON200_FILE, "w", encoding="utf-8") as file:
            for item in _NON200_LINKS:
                link = item[0]
                status_code = item[1]
                file.write(f"{link} - {status_code}\n")

    if _CANONICAL_MISMATCHES:
        with open(CANONICAL_FILE, "w", encoding="utf-8") as file:
            for item in _CANONICAL_MISMATCHES:
                link = item[0]
                canonical_url = item[1]
                file.write(f"{link} - {canonical_url}\n")

    if _NON200_LINKS or _CANONICAL_MISMATCHES:
        raise SystemExit("Обнаружены ошибки в статусах или canonical")

