"""Small HTTP client with retries, backoff, and conditional requests."""

from __future__ import annotations

import http.client
import random
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

USER_AGENT = "claude-info/0.1 (personal offline documentation mirror)"
RETRY_STATUS = {408, 425, 429, 500, 502, 503, 504}


class FetchError(Exception):
    pass


@dataclass
class Response:
    url: str
    status: int
    body: bytes
    etag: str | None
    last_modified: str | None
    content_type: str


def get(
    url: str,
    *,
    etag: str | None = None,
    last_modified: str | None = None,
    attempts: int = 5,
    timeout: float = 60,
) -> Response:
    """GET a URL. Returns status 304 with an empty body when unchanged."""
    headers = {"User-Agent": USER_AGENT, "Accept": "text/markdown, text/plain, */*"}
    if etag:
        headers["If-None-Match"] = etag
    if last_modified:
        headers["If-Modified-Since"] = last_modified
    last_error: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as r:
                return Response(
                    url=r.geturl(),
                    status=r.status,
                    body=r.read(),
                    etag=r.headers.get("ETag"),
                    last_modified=r.headers.get("Last-Modified"),
                    content_type=r.headers.get("Content-Type", ""),
                )
        except urllib.error.HTTPError as e:
            if e.code == 304:
                return Response(url, 304, b"", etag, last_modified, "")
            if e.code not in RETRY_STATUS:
                raise FetchError(f"{url}: HTTP {e.code}") from e
            last_error = e
            retry_after = e.headers.get("Retry-After", "")
            delay = float(retry_after) if retry_after.isdigit() else 0
        except (urllib.error.URLError, http.client.HTTPException, TimeoutError,
                ConnectionError, OSError, ValueError) as e:
            # HTTPException covers truncated bodies (IncompleteRead) and
            # garbled status lines; ValueError covers malformed URLs/headers.
            last_error = e
            delay = 0
        if attempt == attempts - 1:
            break  # no point waiting after the last try
        delay = max(delay, 2**attempt + random.random())
        time.sleep(min(delay, 60))
    raise FetchError(f"{url}: failed after {attempts} attempts: {last_error}")
