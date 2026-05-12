from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Engine:
    key: str
    name: str
    tor_required: bool
    filtered: bool
    config: dict[str, Any]


def list_engines(search_engines: dict[str, dict[str, Any]]) -> list[Engine]:
    out: list[Engine] = []
    for key, cfg in search_engines.items():
        out.append(
            Engine(
                key=key,
                name=str(cfg.get("name", key)),
                tor_required=bool(cfg.get("tor_required", False)),
                filtered=bool(cfg.get("filtered", True)),
                config=cfg,
            )
        )
    return out


def get_engine(search_engines: dict[str, dict[str, Any]], key: str) -> Engine | None:
    cfg = search_engines.get(key)
    if not cfg:
        return None
    return Engine(
        key=key,
        name=str(cfg.get("name", key)),
        tor_required=bool(cfg.get("tor_required", False)),
        filtered=bool(cfg.get("filtered", True)),
        config=cfg,
    )

