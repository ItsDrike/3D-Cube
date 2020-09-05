import unittest
from math import sqrt

from src.exceptions import DimensionError
from src.vector import Vector


class TestVector(unittest.TestCase):
    def test_x_distance(self) -> None:
        v1 = Vector(0, 0)
        v2 = Vector(10, 0)
        distance = v1.distance(v2)
        self.assertEqual(distance, 10)

    def test_y_distance(self) -> None:
        v1 = Vector(0, 0)
        v2 = Vector(0, 10)
        distance = v1.distance(v2)
        self.assertEqual(distance, 10)

    def test_xy_distance(self) -> None:
        v1 = Vector(0, 0)
        v2 = Vector(4, 4)
        distance = v1.distance(v2)
        self.assertEqual(distance, sqrt(32))

    def test_single_negative_distance(self) -> None:
        v1 = Vector(0, 0)
        v2 = Vector(4, -4)
        distance = v1.distance(v2)
        self.assertEqual(distance, sqrt(32))

    def test_both_negative_distance(self) -> None:
        v1 = Vector(0, 0)
        v2 = Vector(-4, -4)
        distance = v1.distance(v2)
        self.assertEqual(distance, sqrt(32))

    def test_add(self) -> None:
        v1 = Vector(-1, 5)
        v2 = Vector(2, 5)
        ans = v1 + v2
        self.assertEqual(ans, Vector(1, 10))

    def test_add_different_dimensions(self) -> None:
        v1 = Vector(1, 2)
        v2 = Vector(1, 1, 1)
        self.assertRaises(DimensionError, lambda: v1 + v2)

    def test_sub(self) -> None:
        v1 = Vector(5, 8)
        v2 = Vector(-2, 10)
        ans = v1 - v2
        self.assertEqual(ans, Vector(7, -2))

    def test_sub_different_dimensions(self) -> None:
        v1 = Vector(1, 2)
        v2 = Vector(1, 1, 1)
        self.assertRaises(DimensionError, lambda: v1 - v2)

    def test_vec_mult(self) -> None:
        v1 = Vector(3, 8)
        v2 = Vector(-2, 2)
        self.assertRaises(TypeError, lambda: v1 * v2)

    def test_float_mult(self) -> None:
        v1 = Vector(3, 8)
        ans = v1 * 2.5
        self.assertEqual(ans, Vector(7.5, 20))

    def test_vec_div(self) -> None:
        v1 = Vector(3, 8)
        v2 = Vector(-2, 2)
        self.assertRaises(TypeError, lambda: v1 / v2)

    def test_float_div(self) -> None:
        v1 = Vector(4, 8)
        ans = v1 / 2.5
        self.assertEqual(ans, Vector(1.6, 3.2))

    def test_vec_floor_div(self) -> None:
        v1 = Vector(3, 8)
        v2 = Vector(-2, 2)
        self.assertRaises(TypeError, lambda: v1 // v2)

    def test_float_floor_div(self) -> None:
        v1 = Vector(4, 8)
        ans = v1 // 2.5
        self.assertEqual(ans, Vector(1, 3))

    def test_set_item(self) -> None:
        v = Vector(1, 2)
        v[0] = 2
        self.assertEqual(v.x, 2)

    def test_del_item(self) -> None:
        v = Vector(1, 2, 3)
        del v[2]
        self.assertEqual(v.dimensions, 2)
