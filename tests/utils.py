from settings import SITES, TIMEOUT, HEADERS
import requests
import xml.etree.ElementTree as xml_tree
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from urllib.parse import urlsplit, urlunsplit
import warnings

# Отключаем предупреждение BeautifulSoup
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Сессия с заголовком
session = requests.Session()
session.headers.update(HEADERS)

# Получение ответа
def fetch(url: str, *, head: bool = False) -> tuple[int | None, bytes]:
    try:
        response = session.head(url, timeout=TIMEOUT, allow_redirects=True) if head else session.get(url, timeout=TIMEOUT)
        return response.status_code, response.content
    except requests.RequestException:
        return None, b""

# Загрузка ссылок из sitemap и custom_urls
def load_sitemap() -> list[str]:
    all_links = []

    for site_config in SITES:
        site_root = site_config["root"].rstrip("/")
        sitemap_path = site_config.get("sitemap")
        custom_paths = site_config.get("custom_urls", [])

        if sitemap_path:
            status_code, body = fetch(site_root + sitemap_path)
            if status_code == 200:
                try:
                    tree = xml_tree.fromstring(body)
                    namespace = {"sm": tree.tag.split('}')[0].strip('{')}
                    urls = [node.text.rstrip("/") for node in tree.findall(".//sm:loc", namespace)]
                    urls = [url for url in urls if not url.endswith(".xml")]
                    all_links.extend(urls)
                except Exception as parse_error:
                    print(f"[warn] Не удалось распарсить sitemap для {site_root}: {parse_error}")
        else:
            all_links.append(site_root)

        for custom_path in custom_paths:
            all_links.append(site_root + custom_path)

    return all_links

# Извлечение тега <link rel="canonical">
def extract_canonical(html_bytes: bytes) -> str | None:
    soup = BeautifulSoup(html_bytes, features="html.parser")
    tag = soup.find("link", rel=lambda value: value and "canonical" in value.lower())
    return tag["href"].strip() if tag and tag.has_attr("href") else None

# Нормализация урлов: убираем лишние слеши, query
def _norm(url: str) -> str:
    parsed = urlsplit(url)
    normalized_path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), normalized_path, "", ""))
