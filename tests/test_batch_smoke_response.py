import http.client
import socket
import threading
import unittest
from http.server import HTTPServer

from tests.test_app import Quiet, handler_class


class BatchSmokeResponseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = type("QuietHandler", (Quiet, handler_class()), {})
        cls.server = HTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def assertCompleteResponse(self, path, expected):
        with socket.create_connection(self.server.server_address, timeout=5) as connection:
            request = f"GET {path} HTTP/1.0\r\nHost: localhost\r\nConnection: close\r\n\r\n"
            connection.sendall(request.encode("ascii"))
            with connection.makefile("rb") as response:
                status = response.readline()
                headers = http.client.parse_headers(response)
                # Read through connection close, including bytes beyond Content-Length.
                body = response.read()
        self.assertEqual(status.split()[1], b"200")
        self.assertEqual(headers.get_content_type(), "text/plain")
        self.assertEqual(int(headers["Content-Length"]), len(expected))
        self.assertEqual(body, expected)

    def test_single_response_contains_only_the_greeting(self):
        self.assertCompleteResponse(
            "/batch-smoke/greeting?name=Ada", b"Hello, Ada!"
        )

    def test_batch_response_contains_only_the_greetings(self):
        self.assertCompleteResponse(
            "/batch-smoke/greetings?name=Lin&name=Ada&name=Lin",
            b"Hello, Lin!\nHello, Ada!\nHello, Lin!",
        )
