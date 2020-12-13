import typing as t

import pygame

from src.matrix import Matrix
from src.util import Colors, NUMBER


class Point2D:
    def __init__(self, x: NUMBER, y: NUMBER):
        self.x = x
        self.y = y

        self.matrix = Matrix([[x], [y]])

    def __setattr__(self, name: str, value: t.Any) -> None:
        """
        In case attributes `x` or `y` are reset, make sure to also
        reset the internal `matrix` attribute to match them.

        In case `matrix` is reset, make sure to also reset the internal
        `x` and `y` attributes to match it.
        """
        if all((
            name in ("x", "y"),
            hasattr(self, "x"), hasattr(self, "y")
        )):
            super().__setattr__("matrix", Matrix([[self.x], [self.y]]))

        if name == "matrix":
            if not isinstance(value, Matrix):
                raise TypeError(f"`matrix` parameter must be an instance of `{Matrix.__class__}`")
            if value.shape != (2, 1):
                raise ValueError(f"Dimensions of `matrix` parameter must be (2, 1), not {value.shape}")

            super().__setattr__("x", value[0, 0])
            super().__setattr__("y", value[1, 0])

        super().__setattr__(name, value)

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

    def rotate(self, clockwise: bool, angle: NUMBER, origin: "Point2D" = None) -> "Point2D":
        """
        Rotate point `clockwise` with specified `angle`.
        In case you want to use different origin than (0, 0),
        you can specify `origin` which will be a `Point2D` object.
        """
        if origin is None:
            origin = self.__class__(x=0, y=0)

        rotation_matrix = Matrix.get_2d_rotation_matrix(clockwise, angle)
        rotated_matrix = rotation_matrix * (self.matrix - origin.matrix) + origin.matrix
        return self.__class__(rotated_matrix[0, 0], rotated_matrix[1, 0])

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

        In case `matrix` is reset, make sure to also reset the internal
        `x`, `y` and `z` attributes to match it.
        """
        super().__setattr__(name, value)

        if all((
            name in ("x", "y", "z"),
            hasattr(self, "x"), hasattr(self, "y"), hasattr(self, "z")
        )):
            super().__setattr__("matrix", Matrix([[self.x], [self.y], [self.z]]))

        if name == "matrix":
            if not isinstance(value, Matrix):
                raise TypeError(f"`matrix` parameter must be an instance of `{Matrix.__class__}`")
            if value.shape != (3, 1):
                raise ValueError(f"Dimensions of `matrix` parameter must be (3, 1), not {value.shape}")

            super().__setattr__("x", value[0, 0])
            super().__setattr__("y", value[1, 0])
            super().__setattr__("z", value[2, 0])

        super().__setattr__(name, value)

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

    def rotate(self, axis: t.Literal["x", "y", "z"], angle: NUMBER, origin: "Point3D" = None) -> "Point3D":
        """
        Rotate point along given `axis` with specified `angle`.
        In case you want to use different origin than (0, 0, 0),
        you can specify `origin` which will be a `Point3D` object.
        """
        if origin is None:
            origin = self.__class__(x=0, y=0, z=0)

        rotation_matrix = Matrix.get_3d_rotation_matrix(axis, angle)
        rotated_matrix = rotation_matrix * (self.matrix - origin.matrix) + origin.matrix
        return self.__class__(rotated_matrix[0, 0], rotated_matrix[1, 0], rotated_matrix[2, 0])

    def __repr__(self) -> str:
        return f"<3D Point (x={self.x},y={self.y},z={self.z})>"
