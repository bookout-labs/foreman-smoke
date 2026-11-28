"""The smallest app foreman-smoke has: an HTTP server on 127.0.0.1:8080 that answers GET /health with ok."""

from http.server import BaseHTTPRequestHandler, HTTPServer


class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/health":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok\n")


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8080), Health).serve_forever()
