"""
Camada de serviço para APIs externas de jogos (RAWG, IGDB).
Chaves via variáveis de ambiente — nunca commitar segredos.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class GameImportPreview:
    title: str
    description: str
    cover_url: str | None
    release_date: str | None
    developer: str
    publisher: str
    genres: list[str]
    platforms: list[str]
    raw: dict[str, Any]


class ExternalGameAPIError(Exception):
    pass


class RawgGameService:
    BASE_URL = "https://api.rawg.io/api"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or getattr(settings, "RAWG_API_KEY", "")

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str, page_size: int = 10) -> list[GameImportPreview]:
        if not self.enabled:
            return []
        try:
            response = requests.get(
                f"{self.BASE_URL}/games",
                params={"key": self.api_key, "search": query, "page_size": page_size},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            logger.warning("RAWG search failed: %s", exc)
            raise ExternalGameAPIError("Não foi possível consultar a API de jogos.") from exc

        results = []
        for item in data.get("results", []):
            results.append(self._normalize(item))
        return results

    def _normalize(self, item: dict[str, Any]) -> GameImportPreview:
        developers = [d.get("name", "") for d in item.get("developers", []) if d.get("name")]
        publishers = [p.get("name", "") for p in item.get("publishers", []) if p.get("name")]
        genres = [g.get("name", "") for g in item.get("genres", []) if g.get("name")]
        platforms = [
            p.get("platform", {}).get("name", "")
            for p in item.get("platforms", [])
            if p.get("platform", {}).get("name")
        ]
        return GameImportPreview(
            title=item.get("name", ""),
            description=item.get("description_raw") or item.get("description") or "",
            cover_url=item.get("background_image"),
            release_date=item.get("released"),
            developer=developers[0] if developers else "",
            publisher=publishers[0] if publishers else "",
            genres=genres,
            platforms=platforms,
            raw=item,
        )


def get_game_api_service():
    """Factory — extensível para IGDB no futuro."""
    return RawgGameService()
