"""api — a stdlib HTTP JSON front-end over the task domain (no dependencies).

Routes:
  GET    /tasks            list tasks        (optional ?status=todo|done)
  POST   /tasks            create a task     body: {"title": "..."}
  DELETE /tasks/{id}       delete a task

Run:  python -m taskservice.api --file tasks.json --port 8000

The routing lives in `dispatch()` — a pure function returning (status, payload) —
so it can be tested without starting a server. The HTTP handler is a thin adapter.
"""
import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from . import domain, storage

_TASK_ID = re.compile(r"^/tasks/(\d+)$")


def dispatch(method, path, body, file):
    """Route one request. Returns (status_code, json_serializable_payload)."""
    parsed = urlparse(path)
    route = parsed.path
    query = parse_qs(parsed.query)

    try:
        tasks = storage.load(file)
    except storage.StorageError as exc:
        return 500, {"error": str(exc)}

    if route == "/tasks":
        if method == "GET":
            status = query.get("status", [None])[0]
            try:
                return 200, domain.list_tasks(tasks, status)
            except domain.TaskError as exc:
                return 400, {"error": str(exc)}
        if method == "POST":
            title = (body or {}).get("title")
            try:
                task = domain.add(tasks, title)
            except domain.TaskError as exc:
                return 400, {"error": str(exc)}
            storage.save(file, tasks)
            return 201, task

    match = _TASK_ID.match(route)
    if match and method == "DELETE":
        task_id = int(match.group(1))
        try:
            domain.delete(tasks, task_id)
        except domain.TaskError as exc:
            return 404, {"error": str(exc)}
        storage.save(file, tasks)
        return 200, {"deleted": task_id}

    return 404, {"error": "not found"}


class Handler(BaseHTTPRequestHandler):
    file = "tasks.json"

    def _respond(self, method):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw) if raw else None
        except (json.JSONDecodeError, ValueError):
            status, payload = 400, {"error": "request body is not valid JSON"}
        else:
            status, payload = dispatch(method, self.path, body, self.file)
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._respond("GET")

    def do_POST(self):
        self._respond("POST")

    def do_DELETE(self):
        self._respond("DELETE")

    def log_message(self, *args):  # keep the test/lab output quiet
        pass


def run(file="tasks.json", host="127.0.0.1", port=8000):
    Handler.file = file
    server = HTTPServer((host, port), Handler)
    print(f"task-service API on http://{host}:{port}  (store: {file})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="taskservice.api")
    parser.add_argument("--file", default="tasks.json")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    run(file=args.file, host=args.host, port=args.port)
