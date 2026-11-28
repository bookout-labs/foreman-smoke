import http.client
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

import app


def _handler_class():
    # The request handler app.py serves with, found by type so the tests do not
    # depend on what the class is called.
    handlers = [
        value
        for value in vars(app).values()
        if isinstance(value, type)
        and issubclass(value, BaseHTTPRequestHandler)
        and value.__module__ == app.__name__
    ]
    if len(handlers) != 1:
        raise AssertionError(f"expected one request handler in app.py, found {handlers}")
    return handlers[0]


class GreetEndpointTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), _handler_class())
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def get(self, path):
        # http.client sends the path exactly as written, so percent-encoding
        # and repeated parameters reach the server untouched.
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            return response.status, response.getheader("Content-Type"), response.read()
        finally:
            connection.close()

    def assertAnswers(self, path, status, body):
        with self.subTest(path=path):
            got_status, content_type, got_body = self.get(path)
            self.assertEqual(got_status, status)
            self.assertEqual(content_type, "text/plain")
            self.assertEqual(got_body, body)

    def test_greets_each_name_as_plain_text(self):
        self.assertAnswers("/greet?name=Ada&name=Bo", 200, b"Hello, Ada. | Hello, Bo.\n")

    def test_greets_with_the_punctuation_parameter(self):
        self.assertAnswers(
            "/greet?name=Ada&name=Bo&punctuation=!", 200, b"Hello, Ada! | Hello, Bo!\n"
        )
        self.assertAnswers(
            "/greet?name=Ada&name=Bo&punctuation=%3F", 200, b"Hello, Ada? | Hello, Bo?\n"
        )

    def test_url_decodes_names_and_keeps_query_order(self):
        self.assertAnswers(
            "/greet?name=Bo&name=Ada%20Lovelace",
            200,
            b"Hello, Bo. | Hello, Ada Lovelace.\n",
        )

    def test_greets_a_percent_encoded_non_ascii_name_in_utf8(self):
        self.assertAnswers(
            "/greet?name=Ada%C2%B2", 200, "Hello, Ada².\n".encode("utf-8")
        )

    def test_rejects_a_request_without_names(self):
        self.assertAnswers("/greet", 400, b"names must not be empty\n")

    def test_rejects_an_invalid_name_with_its_position(self):
        self.assertAnswers(
            "/greet?name=Ada&name=R2D2", 400, b"name 2: name must not contain digits\n"
        )
        self.assertAnswers(
            "/greet?name=Ada&name=", 400, b"name 2: name must not be empty\n"
        )

    def test_rejects_invalid_punctuation(self):
        self.assertAnswers(
            "/greet?name=Ada&punctuation=x", 400, b"punctuation must be one of . ! ?\n"
        )


if __name__ == "__main__":
    unittest.main()
