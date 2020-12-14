from contextlib import suppress

import pygame
from loguru import logger

from src.config import Simulation, Window
from src.cube import Cube
from src.point import Point2D
from src.util import Colors


class Game:
    def __init__(self, width: int, height: int, fps: int) -> None:
        self.size = self.width, self.height = width, height

        pygame.init()
        self.surface = pygame.display.set_mode(self.size)
        self.fps_clock = pygame.time.Clock()
        self.tick_rate = fps

        self.running = True

    def handle_user_event(self) -> None:
        """Handle pygame events (f.e.: quit, click)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False

    def redraw_screen(self) -> None:
        """
        Redraw everything on the screen.

        This does not update the screen, it only redraws it.
        """
        self.surface.fill(Colors.GREY)

        if Simulation.orthographic:
            projected_shape = self.cube.orthographic_project()
            scale = Simulation.cube_scale
        else:
            projected_shape = self.cube.perspective_project(Simulation.projection_distance)
            scale = Simulation.cube_scale * Simulation.projection_distance

        self.cube.draw(
            self.surface,
            projected_shape=projected_shape,
            scale=scale,
            point_size=5,
            point_color=Colors.WHITE,
            side_width=2,
            side_color=Colors.RED,
        )

    def update_screen(self, tick: bool = True) -> None:
        """
        Update the screen accordingly to `redraw_screen`
        also check for user event and tick (if not specified otherwise)
        """

        self.handle_user_event()

        if not self.running:
            return

        self.redraw_screen()
        pygame.display.update()
        if tick:
            self.fps_clock.tick(self.tick_rate)

    def main(self) -> None:
        # Initial setup
        logger.info("Starting game")
        self.cube = Cube(
            middle=Point2D(self.width / 2, self.height / 2),
            radius=1
        )

        # Main game loop
        while self.running:
            self.cube.rotate("x", 1)
            self.cube.rotate("y", 1)
            self.cube.rotate("z", 1)
            self.update_screen()


game = Game(Window.width, Window.height, Window.tick_rate)

with suppress(KeyboardInterrupt):
    game.main()

logger.info("Game Stopped")
pygame.quit()
