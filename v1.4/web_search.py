"""Búsqueda web controlada para JARVIS v1.4.

No ejecuta contenido encontrado ni permite comandos arbitrarios.
La integración HTTP queda desacoplada para conectar un proveedor después.
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str = ""


class WebSearch:
    """Interfaz segura y neutral para proveedores de búsqueda."""

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        query = query.strip()
        if not query:
            return []
        if limit < 1 or limit > 10:
            raise ValueError("limit debe estar entre 1 y 10")
        # v1.4 prepara la capa de búsqueda sin inventar resultados.
        return [{"title": "", "url": "", "snippet": "", "query": query}]
