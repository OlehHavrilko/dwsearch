from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _load_toml(path: Path) -> dict[str, Any]:
    try:
        import tomllib  # py>=3.11
    except ModuleNotFoundError:  # py<=3.10
        import tomli as tomllib  # type: ignore
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)  # type: ignore[arg-type]
        else:
            out[k] = v
    return out


@dataclass(frozen=True)
class RuntimeConfig:
    socks5_url: str = "socks5h://localhost:9050"
    timeout_s: float = 20.0
    retries: int = 2
    backoff_s: float = 0.6
    default_engine: str = "ahmia"
    default_amount: int = 10
    concurrency: int = 6
    headers_preset: str = "random"
    profile: str = "uncensored"
    extra: dict[str, Any] = field(default_factory=dict)


def load_runtime_config(path: str | None, profile: str | None) -> RuntimeConfig:
    data: dict[str, Any] = {}
    if path:
        p = Path(path).expanduser()
        if p.is_file():
            data = _load_toml(p)

    profiles = data.get("profiles", {}) if isinstance(data.get("profiles", {}), dict) else {}
    prof = profile or data.get("profile") or "uncensored"
    selected = profiles.get(prof, {}) if isinstance(profiles.get(prof, {}), dict) else {}

    merged = _deep_merge(data.get("defaults", {}) if isinstance(data.get("defaults", {}), dict) else {}, selected)

    return RuntimeConfig(
        socks5_url=str(merged.get("socks5_url", "socks5h://localhost:9050")),
        timeout_s=float(merged.get("timeout_s", 20.0)),
        retries=int(merged.get("retries", 2)),
        backoff_s=float(merged.get("backoff_s", 0.6)),
        default_engine=str(merged.get("default_engine", "ahmia")),
        default_amount=int(merged.get("default_amount", 10)),
        concurrency=int(merged.get("concurrency", 6)),
        headers_preset=str(merged.get("headers_preset", "random")),
        profile=str(prof),
        extra={k: v for k, v in merged.items() if k not in {
            "socks5_url", "timeout_s", "retries", "backoff_s", "default_engine",
            "default_amount", "concurrency", "headers_preset",
        }},
    )

