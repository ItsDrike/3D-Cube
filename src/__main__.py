from contextlib import suppress

import pygame

from src.config import Window
from src.util import Colors


class Game:
    def __init__(self, width: int, height: int, fps: int) -> None:
        self.size = self.width, self.height = width, height

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
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
        Redraw all cells on the screen.

        This does not update the screen, it only redraws it.
        """
        self.screen.fill(Colors.GREY)

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
        # Main game loop
        while self.running:
            self.update_screen()


game = Game(Window.width, Window.height, Window.tick_rate)

with suppress(KeyboardInterrupt):
    game.main()

print("\nStopped")
pygame.quit()
