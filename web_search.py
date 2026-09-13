"""Búsqueda web real y controlada para JARVIS v1.4.

Usa la API pública de DuckDuckGo Instant Answer mediante HTTPS y no ejecuta
contenido devuelto por Internet.
"""

import json
from dataclasses import dataclass
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""


class WebSearch:
    endpoint = "https://api.duckduckgo.com/?format=json&no_html=1&skip_disambig=1&q="

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        query = query.strip()
        if not query:
            return []
        if not 1 <= limit <= 10:
            raise ValueError("limit debe estar entre 1 y 10")

        request = Request(
            self.endpoint + quote_plus(query),
            headers={"User-Agent": "JARVIS/1.4"},
        )
        with urlopen(request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))

        results: list[SearchResult] = []
        if payload.get("AbstractURL"):
            results.append(SearchResult(
                payload.get("Heading", query),
                payload["AbstractURL"],
                payload.get("AbstractText", ""),
            ))
        for item in payload.get("RelatedTopics", []):
            if len(results) >= limit:
                break
            if "FirstURL" in item:
                results.append(SearchResult(
                    item.get("Text", "Resultado"),
                    item["FirstURL"],
                    item.get("Text", ""),
                ))
        return results
