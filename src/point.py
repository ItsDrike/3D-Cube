import typing as t

import pygame

from src.matrix import Matrix
from src.util import Colors, NUMBER


class Point2D:
    def __init__(self, x: NUMBER, y: NUMBER):
        self.x = x
        self.y = y

        self.matrix = Matrix([[x], [y]])

    def draw(
        self,
        surface: pygame.Surface,
        position: t.List[NUMBER] = None,
        color: Colors.ColorType = Colors.WHITE,
        size: NUMBER = 5,
        scale: NUMBER = 1
    ) -> None:
        """
        Draw the point onto pygame `surface`,
        - use `position` as a true center position of given point as pygame center isn't in
        true screen center (i.e. to center object pass fix=[WIDTH//2, HEIGHT//2]).
        - use `scale` to scale the point up, this will be used as a constant
        which will multiply the point on both `x` and `y` axis.
        - Use `size` for the point radius size.
        - Use `color` to specify point color.
        """
        if position is None:
            position = [0, 0]

        pos = [self.x * scale + position[0], self.y * scale + position[1]]
        pygame.draw.circle(surface, color, pos, size)

    def __setattr__(self, name: str, value: t.Any) -> None:
        super().__setattr__(name, value)

        if all((
            name in ("x", "y"),
            hasattr(self, "x"), hasattr(self, "y")
        )):
            self.matrix = Matrix([[self.x], [self.y]])

    def __repr__(self) -> str:
        return f"<2D Point (x={self.x},y={self.y})>"


class Point3D:
    def __init__(self, x: NUMBER, y: NUMBER, z: NUMBER):
        self.x = x
        self.y = y
        self.z = z

        self.matrix = Matrix([[x], [y], [z]])

    def __setattr__(self, name: str, value: t.Any) -> None:
        """
        In case attributes `x`/`y`/`z` are reset, make sure to also
        reset the internal `matrix` attribute to match them.
        """
        super().__setattr__(name, value)

        if all((
            name in ("x", "y", "z"),
            hasattr(self, "x"), hasattr(self, "y"), hasattr(self, "z")
        )):
            self.matrix = Matrix([[self.x], [self.y], [self.z]])

    def project(self, scale: NUMBER = 1) -> Point2D:
        """
        Project given 3D point into 2D by multiplying
        projection matrix by the point position matrix.
        """
        projection_matrix = Matrix.get_projection_matrix(
            in_dimensions=3,  # 3D Point
            out_dimensions=2,  # Project back to 2D
            scale=scale
        )
        projected_matrix = projection_matrix @ self.matrix
        return Point2D(x=projected_matrix[0, 0], y=projected_matrix[1, 0])

    def orthographic_project(self) -> Point2D:
        """
        Project given 3D point into 2D orthographically.
        This means `z` value will simply be ignored
        """
        return self.project(scale=1)

    def perspective_project(self, distance: NUMBER) -> Point2D:
        """
        Project given 3D point into 2D using perspective.
        This means the point will be scaled based on it's
        depth (`z` value) to produce more realistic projection.
        (i.e. point gets smaller as `z` is further away.)
        """
        perspective_scale = 1 / (distance - self.z)
        return self.project(scale=perspective_scale)

    def __repr__(self) -> str:
        return f"<3D Point (x={self.x},y={self.y},z={self.z})>"
