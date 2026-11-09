"""Tests for claude_info.http: retries, backoff, conditional requests.

Most tests run against a real local http.server in a thread; a few stub
urllib.request.urlopen to inject failures a server can't easily produce.
time.sleep is replaced so backoff costs nothing.
"""

from __future__ import annotations

import http.client
import io
import threading
import urllib.error
import urllib.request
from email.message import Message
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from claude_info import http as h


@pytest.fixture
def sleeps(monkeypatch):
    calls: list[float] = []
    monkeypatch.setattr(h.time, "sleep", lambda s: calls.append(s))
    return calls


@pytest.fixture(autouse=True)
def no_proxy(monkeypatch):
    # A proxy from the environment must not intercept requests to 127.0.0.1.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    monkeypatch.setattr(urllib.request, "_opener", opener)


class Server:
    """Serves a scripted sequence of responses per path."""

    def __init__(self):
        self.script: dict[str, list] = {}
        self.requests: list[tuple[str, dict]] = []
        server = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                server.requests.append((self.path, dict(self.headers)))
                steps = server.script.get(self.path, [])
                step = steps.pop(0) if len(steps) > 1 else (steps[0] if steps else (404, {}, b""))
                status, headers, body = step
                if status == "truncate":
                    self.send_response(200)
                    self.send_header("Content-Length", str(len(body) + 100))
                    self.end_headers()
                    self.wfile.write(body)
                    self.wfile.flush()
                    self.close_connection = True
                    return
                self.send_response(status)
                for k, v in headers.items():
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, args=(0.01,), daemon=True)
        self.thread.start()

    def hits(self, path: str) -> int:
        return sum(1 for p, _ in self.requests if p == path)

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


@pytest.fixture
def server():
    s = Server()
    yield s
    s.close()


def test_plain_get_returns_body_and_validators(server, sleeps):
    server.script["/a.md"] = [(200, {"ETag": '"v1"', "Last-Modified": "Wed, 01 Oct 2026 00:00:00 GMT",
                                     "Content-Type": "text/markdown"}, b"# Hi\n")]
    r = h.get(server.base + "/a.md")
    assert (r.status, r.body, r.etag, r.content_type) == (200, b"# Hi\n", '"v1"', "text/markdown")
    assert r.last_modified == "Wed, 01 Oct 2026 00:00:00 GMT"
    assert r.url == server.base + "/a.md"
    assert sleeps == []
    headers = server.requests[0][1]
    assert headers["User-Agent"] == h.USER_AGENT
    assert "If-None-Match" not in headers and "If-Modified-Since" not in headers


def test_conditional_request_and_304(server, sleeps):
    server.script["/a.md"] = [(304, {}, b"")]
    r = h.get(server.base + "/a.md", etag='"v1"', last_modified="Wed, 01 Oct 2026 00:00:00 GMT")
    assert r.status == 304 and r.body == b""
    # The caller's validators come back so they can be stored again.
    assert r.etag == '"v1"' and r.last_modified == "Wed, 01 Oct 2026 00:00:00 GMT"
    headers = server.requests[0][1]
    assert headers["If-None-Match"] == '"v1"'
    assert headers["If-Modified-Since"] == "Wed, 01 Oct 2026 00:00:00 GMT"
    assert sleeps == [] and server.hits("/a.md") == 1


@pytest.mark.parametrize("status", [500, 502, 503, 504, 429, 408])
def test_retries_transient_status_then_succeeds(server, sleeps, status):
    server.script["/a.md"] = [(status, {}, b"oops"), (status, {}, b"oops"), (200, {}, b"ok")]
    r = h.get(server.base + "/a.md")
    assert r.status == 200 and r.body == b"ok"
    assert server.hits("/a.md") == 3
    assert len(sleeps) == 2
    # Exponential backoff with jitter: 2**attempt + [0, 1).
    assert 1 <= sleeps[0] < 2 and 2 <= sleeps[1] < 3


@pytest.mark.parametrize("status", [404, 410, 403, 400, 501])
def test_no_retry_on_permanent_status(server, sleeps, status):
    server.script["/a.md"] = [(status, {}, b"nope")]
    with pytest.raises(h.FetchError, match=f"HTTP {status}"):
        h.get(server.base + "/a.md")
    assert server.hits("/a.md") == 1
    assert sleeps == []


def test_404_message_is_what_fetch_relies_on(server, sleeps):
    # fetch._fetch_page tells "gone" from "error" by "HTTP 404" / "HTTP 410".
    server.script["/gone.md"] = [(404, {}, b"")]
    with pytest.raises(h.FetchError) as e:
        h.get(server.base + "/gone.md")
    assert "HTTP 404" in str(e.value)


def test_gives_up_after_attempts(server, sleeps):
    server.script["/a.md"] = [(503, {}, b"down")]
    with pytest.raises(h.FetchError, match="failed after 4 attempts") as e:
        h.get(server.base + "/a.md", attempts=4)
    assert server.hits("/a.md") == 4
    assert "503" in str(e.value)


def test_retry_after_is_honoured_and_capped(server, sleeps):
    server.script["/a.md"] = [(429, {"Retry-After": "7"}, b""), (429, {"Retry-After": "3600"}, b""),
                              (429, {"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}, b""),
                              (200, {}, b"ok")]
    assert h.get(server.base + "/a.md").body == b"ok"
    assert sleeps[0] == 7  # longer than the backoff of 1-2 s
    assert sleeps[1] == 60  # capped
    assert 4 <= sleeps[2] < 5  # an HTTP-date is ignored: plain backoff


def test_retries_truncated_body(server, sleeps):
    server.script["/a.md"] = [("truncate", {}, b"# Half a pa"), (200, {}, b"# Whole page\n")]
    r = h.get(server.base + "/a.md")
    assert r.body == b"# Whole page\n"
    assert server.hits("/a.md") == 2 and len(sleeps) == 1


def test_truncated_every_time_raises_fetch_error(server, sleeps):
    server.script["/a.md"] = [("truncate", {}, b"partial")]
    with pytest.raises(h.FetchError, match="failed after 3 attempts"):
        h.get(server.base + "/a.md", attempts=3)
    assert server.hits("/a.md") == 3


def test_connection_refused_raises_fetch_error(sleeps):
    s = Server()
    base = s.base
    s.close()  # nothing listens on that port any more
    with pytest.raises(h.FetchError, match="failed after 2 attempts"):
        h.get(base + "/a.md", attempts=2)


# -- stubbed urlopen: failures a local server can't produce reliably ----------


class FakeResponse:
    def __init__(self, body=b"ok", status=200, url="https://x.test/a", headers=None, read_error=None):
        self._body, self.status, self._url = body, status, url
        self.headers = Message()
        for k, v in (headers or {}).items():
            self.headers[k] = v
        self._read_error = read_error

    def read(self):
        if self._read_error:
            raise self._read_error
        return self._body

    def geturl(self):
        return self._url

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def scripted_urlopen(monkeypatch, steps):
    calls = []

    def fake(request, timeout=None):
        calls.append(request)
        step = steps[min(len(calls) - 1, len(steps) - 1)]
        if isinstance(step, BaseException):
            raise step
        return step

    monkeypatch.setattr(urllib.request, "urlopen", fake)
    return calls


def http_error(code, headers=None):
    m = Message()
    for k, v in (headers or {}).items():
        m[k] = v
    return urllib.error.HTTPError("https://x.test/a", code, "msg", m, io.BytesIO(b""))


@pytest.mark.parametrize("exc", [
    http.client.IncompleteRead(b"part", 100),
    http.client.RemoteDisconnected("closed"),
    http.client.BadStatusLine("garbage"),
    urllib.error.URLError("dns failure"),
    TimeoutError("timed out"),
    ConnectionResetError("reset"),
    OSError("network unreachable"),
    ValueError("bad header"),
])
def test_transient_exceptions_are_retried(monkeypatch, sleeps, exc):
    calls = scripted_urlopen(monkeypatch, [exc, FakeResponse(b"fine")])
    assert h.get("https://x.test/a").body == b"fine"
    assert len(calls) == 2 and len(sleeps) == 1


@pytest.mark.parametrize("exc", [
    http.client.IncompleteRead(b"part", 100),
    TimeoutError("timed out"),
])
def test_exception_on_every_attempt_becomes_fetch_error(monkeypatch, sleeps, exc):
    calls = scripted_urlopen(monkeypatch, [exc])
    with pytest.raises(h.FetchError, match="failed after 5 attempts"):
        h.get("https://x.test/a")
    assert len(calls) == 5


def test_read_error_inside_response_is_retried(monkeypatch, sleeps):
    bad = FakeResponse(read_error=http.client.IncompleteRead(b"x", 10))
    calls = scripted_urlopen(monkeypatch, [bad, FakeResponse(b"good")])
    assert h.get("https://x.test/a").body == b"good"
    assert len(calls) == 2


def test_304_from_urllib_http_error(monkeypatch, sleeps):
    scripted_urlopen(monkeypatch, [http_error(304)])
    r = h.get("https://x.test/a", etag="e", last_modified="lm")
    assert (r.status, r.body, r.etag, r.last_modified) == (304, b"", "e", "lm")


def test_conditional_headers_sent(monkeypatch, sleeps):
    calls = scripted_urlopen(monkeypatch, [FakeResponse()])
    h.get("https://x.test/a", etag='"abc"')
    assert calls[0].get_header("If-none-match") == '"abc"'
    assert calls[0].get_header("If-modified-since") is None


def test_backoff_is_capped_at_60_seconds(monkeypatch, sleeps):
    scripted_urlopen(monkeypatch, [http_error(503)])
    with pytest.raises(h.FetchError):
        h.get("https://x.test/a", attempts=9)
    assert max(sleeps) <= 60


def test_no_sleep_after_last_attempt(monkeypatch, sleeps):
    scripted_urlopen(monkeypatch, [http_error(503)])
    with pytest.raises(h.FetchError):
        h.get("https://x.test/a", attempts=3)
    assert len(sleeps) == 2
