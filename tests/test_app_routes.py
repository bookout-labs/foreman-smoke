import http.client
import threading
import unittest
from http.server import HTTPServer

from tests.test_app import Quiet, handler_class


class AppRoutesTest(unittest.TestCase):
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

    def test_health_answers_ok_as_plain_text(self):
        status, content_type, body = self.get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(content_type, "text/plain")
        # The whole body read until close must be exactly ok, with nothing after it.
        self.assertEqual(body, b"ok\n")

    def test_other_paths_answer_404(self):
        for path in ("/nope", "/health?x=1", "/greet/", "/"):
            with self.subTest(path=path):
                status, _, _ = self.get(path)
                self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
