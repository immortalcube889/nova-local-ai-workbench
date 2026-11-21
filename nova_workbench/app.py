"""Dependency-free local HTTP application for a safe, inspectable AI-workbench demo."""
from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .storage import MemoryStore
from .tools import inspect_system, plan_file_action

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "static"
DATA = Path(os.environ.get("NOVA_DATA_DIR", ROOT / "data"))
STORE = MemoryStore(DATA / "nova.sqlite3")


def response_for(message: str) -> dict:
    """Transparent non-LLM response illustrating local retrieval safely."""
    matches = STORE.search(message)
    return {
        "response": "This portfolio edition uses local retrieval only. Connect a model provider behind this API in a real deployment; keep approvals outside the model prompt.",
        "matches": matches,
        "model": "not configured in public demo",
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def log_message(self, format, *args):
        return

    def send_json(self, payload: dict, status=HTTPStatus.OK):
        data = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def body(self) -> dict:
        size = int(self.headers.get("Content-Length", "0"))
        if size > 10_000:
            raise ValueError("Request is too large.")
        return json.loads(self.rfile.read(size) or b"{}")

    def do_GET(self):
        route = urlparse(self.path).path
        if route == "/health":
            return self.send_json({"ok": True, "service": "nova-local-ai-workbench"})
        if route == "/api/memories":
            return self.send_json({"items": STORE.recent()})
        return super().do_GET()

    def do_POST(self):
        try:
            data = self.body()
            if self.path == "/api/memories":
                return self.send_json({"item": STORE.add(data.get("text", ""))}, HTTPStatus.CREATED)
            if self.path == "/api/assistant/respond":
                return self.send_json(response_for(data.get("message", "")))
            if self.path == "/api/tools/inspect-system":
                return self.send_json(inspect_system())
            if self.path == "/api/tools/plan-file-action":
                return self.send_json(plan_file_action(data.get("action", ""), data.get("path", "")))
            return self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        except (ValueError, json.JSONDecodeError) as exc:
            return self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)


def main():
    host = os.environ.get("NOVA_HOST", "127.0.0.1")
    port = int(os.environ.get("NOVA_PORT", "8080"))
    print(f"Nova portfolio demo listening at http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
