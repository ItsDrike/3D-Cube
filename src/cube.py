import typing as t

import pygame

from src.point import Point2D, Point3D
from src.util import Colors, NUMBER


class Cube:
    def __init__(self, middle: Point2D, radius: NUMBER):
        self.middle = middle
        self.radius = radius

        self.shape = (
            Point3D(-radius, -radius, -radius),  # A
            Point3D(+radius, -radius, -radius),  # B
            Point3D(+radius, -radius, +radius),  # C
            Point3D(-radius, -radius, +radius),  # D
            Point3D(-radius, +radius, -radius),  # E
            Point3D(+radius, +radius, -radius),  # F
            Point3D(+radius, +radius, +radius),  # G
            Point3D(-radius, +radius, +radius),  # H
        )

    def __getitem__(self, index: int) -> Point3D:
        return self.shape[index]

    @staticmethod
    def edges_2d(shape: t.List[Point2D]) -> t.List[t.Tuple[Point2D, Point2D]]:
        """
        Return edge pairs which are next to each other
        (would have a side between them).
        """
        pairs = []
        for i in range(4):
            pairs.append((shape[i], shape[(i + 1) % 4]))
            pairs.append((shape[i + 4], shape[(i + 1) % 4 + 4]))
            pairs.append((shape[i], shape[i + 4]))

        return pairs

    def rotate(self, axis: t.Literal["x", "y", "z"], angle: NUMBER) -> None:
        for point in self.shape:
            point.rotate(axis, angle)

    def orthographic_project(self) -> t.List[Point2D]:
        projected = []
        for point in self.shape:
            projected.append(point.orthographic_project())

        return projected

    def perspective_project(self, distance: NUMBER) -> t.List[Point2D]:
        projected = []
        for point in self.shape:
            projected.append(point.perspective_project(distance))

        return projected

    def draw(
        self,
        surface: pygame.Surface,
        projection_distance: NUMBER = 5,
        scale: NUMBER = 1,
        point_size: NUMBER = 5,
        point_color: Colors.ColorType = Colors.WHITE,
        side_width: NUMBER = 2,
        side_color: Colors.ColorType = Colors.RED
    ) -> None:
        projected_shape = self.perspective_project(projection_distance)
        edges = self.edges_2d(projected_shape)

        for point in projected_shape:
            point.draw(surface, center=self.middle, scale=scale, size=point_size, color=point_color)

        for point1, point2 in edges:
            point1.connect(surface, point2, center=self.middle, scale=scale, width=side_width, color=side_color)
