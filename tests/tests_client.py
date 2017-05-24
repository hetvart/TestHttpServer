from unittest import TestCase

from client import create_client_parser


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        parser = create_client_parser()
        cls.parser = parser


class TestClient(BaseTest):
    def test_with_no_args(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])
