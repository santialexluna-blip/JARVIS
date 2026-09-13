"""Búsqueda web para JARVIS v2.0, usando HTTPS sin ejecutar contenido remoto."""

from dataclasses import dataclass
from typing import Dict, List
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from html.parser import HTMLParser


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""


class WebSearch:
    def __init__(self, endpoint: str = "https://html.duckduckgo.com/html/?q="):
        self.endpoint = endpoint

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        query = query.strip()
        if not query:
            return []
        if limit < 1 or limit > 10:
            raise ValueError("limit debe estar entre 1 y 10")
        request = Request(self.endpoint + quote_plus(query), headers={"User-Agent": "JARVIS/2.0"})
        try:
            with urlopen(request, timeout=8) as response:
                html = response.read().decode("utf-8", errors="replace")
        except Exception:
            return []

        class Parser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.href = ""
                self.text = []
                self.in_link = False
                self.results = []

            def handle_starttag(self, tag, attrs):
                if tag == "a":
                    attrs = dict(attrs)
                    if "result__a" in attrs.get("class", ""):
                        self.href = attrs.get("href", "")
                        self.text = []
                        self.in_link = True

            def handle_data(self, data):
                if self.in_link:
                    self.text.append(data)

            def handle_endtag(self, tag):
                if tag == "a" and self.in_link:
                    title = " ".join("".join(self.text).split())
                    if self.href:
                        self.results.append({"title": title, "url": self.href, "snippet": ""})
                    self.in_link = False

        parser = Parser()
        parser.feed(html)
        return parser.results[:limit]

    @staticmethod
    def format_results(results: List[Dict[str, str]]) -> str:
        if not results:
            return "No encontré resultados."
        return "\n".join(f"{i}. {r.get('title') or 'Sin título'} — {r.get('url', '')}" for i, r in enumerate(results, 1))
