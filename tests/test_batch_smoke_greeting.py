import http.client
import threading
import unittest
from http.server import HTTPServer

from tests.test_app import Quiet, handler_class


class BatchSmokeGreetingTest(unittest.TestCase):
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

    def assertGreeting(self, path, expected):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            status = response.status
            content_type = response.getheader("Content-Type")
            body = response.read()
        finally:
            connection.close()
        self.assertEqual(status, 200, (path, body))
        self.assertIsNotNone(content_type, path)
        self.assertEqual(content_type.split(";")[0].strip().lower(), "text/plain", path)
        self.assertEqual(body, expected, path)
        return body

    def test_ada_is_plain_text_without_trailing_newline(self):
        self.assertGreeting("/batch-smoke/greeting?name=Ada", b"Hello, Ada!")

    def test_supplied_name_and_case_are_preserved(self):
        for name, expected in (("Lin", b"Hello, Lin!"), ("aDa", b"Hello, aDa!")):
            with self.subTest(name=name):
                self.assertGreeting("/batch-smoke/greeting?name=" + name, expected)

    def test_trims_leading_trailing_and_surrounding_ascii_spaces(self):
        for name in ("%20%20Ada", "Ada%20%20", "%20%20Ada%20%20"):
            with self.subTest(name=name):
                self.assertGreeting("/batch-smoke/greeting?name=" + name, b"Hello, Ada!")


if __name__ == "__main__":
    unittest.main()
