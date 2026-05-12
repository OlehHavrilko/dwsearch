from __future__ import annotations

import time
from typing import Any, Callable, TypeVar

import requests

T = TypeVar("T")


def with_retries(fn: Callable[[], T], retries: int, backoff_s: float) -> T:
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if attempt >= retries:
                break
            time.sleep(backoff_s * (attempt + 1))
    assert last_exc is not None
    raise last_exc


def check_tor_ip(proxy_url: str, timeout_s: float, retries: int, backoff_s: float) -> tuple[bool, str]:
    proxies = {"http": proxy_url, "https": proxy_url}

    def _do() -> tuple[bool, str]:
        r = requests.get("http://check.torproject.org/api/ip", proxies=proxies, timeout=timeout_s)
        if r.status_code != 200:
            return False, "unknown"
        d: Any = r.json()
        return bool(d.get("IsTor", False)), str(d.get("IP", "unknown"))

    return with_retries(_do, retries=retries, backoff_s=backoff_s)

