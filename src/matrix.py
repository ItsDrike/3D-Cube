import typing as t
from math import cos, sin

import numpy as np

from src.util import NUMBER


class Matrix(np.matrix):

    @classmethod
    def get_projection_matrix(cls, in_dimensions: int = 3, out_dimensions: int = 2, scale: NUMBER = 1) -> "Matrix":
        projection_matrix = []
        for i in range(out_dimensions):
            projection_matrix.append([])
            for j in range(in_dimensions):
                if i == j:
                    projection_matrix[i].append(scale)
                else:
                    projection_matrix[i].append(0)

        return cls(projection_matrix)

    @classmethod
    def get_2d_rotation_matrix(cls, clockwise: bool, angle: NUMBER) -> "Matrix":
        if clockwise:
            matrix = [
                [cos(angle), sin(angle)],
                [-sin(angle), cos(angle)]
            ]
        else:
            matrix = [
                [cos(angle), -sin(angle)],
                [sin(angle), cos(angle)]
            ]

        return cls(matrix)

    @classmethod
    def get_3d_rotation_matrix(cls, direction: t.Literal["x", "y", "z"], angle: NUMBER) -> "Matrix":
        if direction == "x":
            matrix = [
                [1, 0, 0],
                [0, cos(angle), -sin(angle)],
                [0, sin(angle), cos(angle)],
            ]
        elif direction == "y":
            matrix = [
                [cos(angle), 0, sin(angle)],
                [0, 1, 0],
                [-sin(angle), 0, cos(angle)],
            ]
        elif direction == "z":
            matrix = [
                [cos(angle), -sin(angle), 0],
                [sin(angle), cos(angle), 0],
                [0, 0, 1],
            ]
        else:
            raise TypeError(f"`direction` must be a literal of `x`/`y`/`z`, not {direction}")

        return cls(matrix)
