from __future__ import annotations

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib import error, parse, request


ROOT = Path(__file__).resolve().parent


class ResourceToolHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = parse.urlparse(self.path)
        if parsed.path == "/proxy":
            query = parse.parse_qs(parsed.query)
            target = (query.get("url") or [""])[0]
            self.proxy_request({"url": target, "method": "GET"})
            return
        super().do_GET()

    def do_POST(self):
        if parse.urlparse(self.path).path != "/proxy":
            self.send_error(404)
            return

        length = int(self.headers.get("content-length", "0") or "0")
        raw_body = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        self.proxy_request(payload)

    def proxy_request(self, payload: dict):
        target = str(payload.get("url") or "")
        parsed = parse.urlparse(target)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            self.send_error(400, "Only http/https URLs are allowed")
            return

        method = str(payload.get("method") or "GET").upper()
        body = payload.get("body")
        body_bytes = body.encode("utf-8") if isinstance(body, str) else None
        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "ResourceSearchTool/0.2",
        }
        for key, value in (payload.get("headers") or {}).items():
            if key.lower() in {"authorization", "content-type", "accept"} and value:
                headers[key] = str(value)

        req = request.Request(target, data=body_bytes, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=8) as resp:
                data = resp.read()
                content_type = resp.headers.get("content-type", "application/octet-stream")
        except error.HTTPError as exc:
            self.send_response(exc.code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            message = {"error": str(exc), "status": exc.code}
            self.wfile.write(json.dumps(message, ensure_ascii=False).encode("utf-8"))
            return
        except Exception as exc:
            self.send_response(502)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            message = {"error": str(exc)}
            self.wfile.write(json.dumps(message, ensure_ascii=False).encode("utf-8"))
            return

        if payload.get("responseType") == "text":
            text = data.decode("utf-8", errors="replace")
            output = json.dumps({"text": text}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(output)))
            self.end_headers()
            self.wfile.write(output)
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), ResourceToolHandler)
    print(f"http://{args.host}:{args.port}/index.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
