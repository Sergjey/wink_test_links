# wink_test_links

Проверка ссылок и canonical на сайте

### Что делает проект:

1. Загружает ссылки из sitemap (`sitemap.xml`) или вручную заданные `custom_urls`
2. Проверяет, что каждая ссылка возвращает статус `200 OK`
3. На HTML-страницах ищет `<link rel="canonical">` и сравнивает с текущим URL
4. Ошибки сохраняются в `.txt` файлы:
   - `non_200.txt` — плохие ссылки
   - `canonical_mismatch.txt` — несовпадающие canonical
5. При наличии ошибок тесты **падают**

---

## 🚀 Как запустить

```bash
git clone https://github.com/your-username/wink_test_links.git
cd wink_test_links
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m pytest -v
