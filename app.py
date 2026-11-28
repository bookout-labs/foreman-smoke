"""The smallest app foreman-smoke has: an HTTP server on 127.0.0.1:8080 that answers
GET /health with ok and GET /greet with greet_all's greeting as plain text."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlsplit

from greet import greet_all


class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_text(200, "ok")
            return
        url = urlsplit(self.path)
        if url.path != "/greet":
            self.send_error(404)
            return
        # Keep blank values so "name=" reaches greet_all as an empty name.
        query = parse_qsl(url.query, keep_blank_values=True)
        names = [value for key, value in query if key == "name"]
        punctuation = next((value for key, value in query if key == "punctuation"), ".")
        try:
            greeting = greet_all(names, punctuation)
        except ValueError as error:
            self.send_text(400, str(error))
            return
        self.send_text(200, greeting)

    def send_text(self, status, text):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write((text + "\n").encode("utf-8"))


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8080), Health).serve_forever()
