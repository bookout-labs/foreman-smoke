import http.client
import threading
import unittest
from http.server import HTTPServer

from tests.test_app import Quiet, handler_class


class BatchSmokeGreetingsTest(unittest.TestCase):
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

    def test_preserves_order_and_duplicates_with_single_newline_separators(self):
        self.assertGreeting(
            "/batch-smoke/greetings?name=Lin&name=Ada&name=Lin",
            b"Hello, Lin!\nHello, Ada!\nHello, Lin!",
        )

    def test_one_name_matches_single_endpoint_for_each_required_value(self):
        for name, expected in (
            ("Ada", b"Hello, Ada!"),
            ("Lin", b"Hello, Lin!"),
            ("aDa", b"Hello, aDa!"),
            ("%20%20Ada%20%20", b"Hello, Ada!"),
        ):
            with self.subTest(name=name):
                batch_body = self.assertGreeting(
                    "/batch-smoke/greetings?name=" + name, expected
                )
                single_body = self.assertGreeting(
                    "/batch-smoke/greeting?name=" + name, expected
                )
                self.assertEqual(batch_body, single_body, name)

    def test_trims_each_value_independently_and_preserves_case(self):
        self.assertGreeting(
            "/batch-smoke/greetings?name=%20Lin&name=aDa%20&name=%20Lin%20",
            b"Hello, Lin!\nHello, aDa!\nHello, Lin!",
        )


if __name__ == "__main__":
    unittest.main()
