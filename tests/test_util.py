import unittest

from src import util


class TestUtil(unittest.TestCase):
    def test_random_color(self) -> None:
        col = util.Colors.random()
        for color in col:
            self.assertTrue(0 <= color <= 256)

    def test_number_remap(self) -> None:
        test_values = (
            ((10, 0, 100, 0, 200), 20),
            ((250, 10, 250, 0, 100), 100),
            ((0, 0, 10000, 50, 100), 50),
        )
        for content, expected_value in test_values:
            with self.subTest(content=content, expected_value=expected_value):
                remapped = util.number_remap(*content)
                self.assertEqual(remapped, expected_value)
