import http.client
import inspect
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

import app


def handler_class():
    # Find the request handler app.py defines, so the tests do not depend on its name.
    for _, value in inspect.getmembers(app, inspect.isclass):
        if (
            issubclass(value, BaseHTTPRequestHandler)
            and value is not BaseHTTPRequestHandler
            and value.__module__ == app.__name__
        ):
            return value
    raise AssertionError("app.py defines no BaseHTTPRequestHandler subclass")


class Quiet:
    def log_message(self, format, *args):
        pass


class AppGreetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = type("QuietHandler", (Quiet, handler_class()), {})
        cls.server = HTTPServer(("127.0.0.1", 0), handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def get(self, path):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            return response.status, response.getheader("Content-Type"), response.read()
        finally:
            connection.close()

    def assertAnswer(self, path, status, body):
        got_status, content_type, got_body = self.get(path)
        self.assertEqual(got_status, status, (path, got_body))
        self.assertIsNotNone(content_type, path)
        self.assertEqual(content_type.split(";")[0].strip().lower(), "text/plain", path)
        self.assertEqual(got_body, body, path)

    def test_greets_each_name_as_plain_text(self):
        self.assertAnswer("/greet?name=Ada&name=Bo", 200, b"Hello, Ada. | Hello, Bo.\n")

    def test_greets_with_punctuation_encoded_or_not(self):
        for path in (
            "/greet?name=Ada&name=Bo&punctuation=!",
            "/greet?name=Ada&name=Bo&punctuation=%21",
        ):
            with self.subTest(path=path):
                self.assertAnswer(path, 200, b"Hello, Ada! | Hello, Bo!\n")

    def test_rejects_missing_names_with_400(self):
        self.assertAnswer("/greet", 400, b"names must not be empty\n")

    def test_rejects_name_with_digits_with_position(self):
        self.assertAnswer(
            "/greet?name=Ada&name=R2D2", 400, b"name 2: name must not contain digits\n"
        )

    def test_empty_name_parameter_counts_as_list_entry(self):
        self.assertAnswer(
            "/greet?name=Ada&name=", 400, b"name 2: name must not be empty\n"
        )

    def test_rejects_invalid_punctuation(self):
        self.assertAnswer(
            "/greet?name=Ada&punctuation=x", 400, b"punctuation must be one of . ! ?\n"
        )


if __name__ == "__main__":
    unittest.main()
