SITES = [
    {
        "root": "https://wink.ru",
        "sitemap": "/sitemaps/sitemap.xml",
    },
    {
        "root": "https://example.com",
        "sitemap": None 
    },
    {
        "root": "https://httpstat.us",
        "sitemap": None,
        "custom_urls": ["/404", "/500", "/403"]
    }
]

NON200_FILE = "non_200.txt"
CANONICAL_FILE = "canonical_mismatch.txt"
TIMEOUT = 10
HEADERS = {"User-Agent": "Mozilla/5.0"}
