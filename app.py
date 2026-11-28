"""The smallest app foreman-smoke has: an HTTP server on 127.0.0.1:8080 that answers
GET /health with ok and GET /greet?name=...&name=...[&punctuation=...] with greet_all."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

from greet import greet_all


class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return
        url = urlsplit(self.path)
        if url.path == "/greet":
            self.greet(url.query)
            return
        self.send_error(404)

    def greet(self, query):
        # keep_blank_values so "name=" counts as an (empty) list entry.
        params = parse_qs(query, keep_blank_values=True)
        names = params.get("name", [])
        punctuation = params.get("punctuation", ["."])[0]
        try:
            body = greet_all(names, punctuation)
        except ValueError as error:
            self.send_text(400, str(error))
            return
        self.send_text(200, body)

    def send_text(self, status, text):
        body = (text + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8080), Health).serve_forever()
