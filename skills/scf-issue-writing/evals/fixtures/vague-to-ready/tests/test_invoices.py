import unittest

from src.invoices import render


class TextOutput(unittest.TestCase):
    def test_text(self):
        rows = [{"id": 1, "customer": "Acme", "total": 120.5}]
        self.assertEqual(render(rows, "text"), "1 Acme 120.5")


if __name__ == "__main__":
    unittest.main()
