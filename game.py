"""
This module serves as the core module of the game, containing essential elements such as the Game class.
"""

import sys
import pygame


class Game:

    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Spider Smash")

    @staticmethod
    def handle_close_event() -> None:

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def run(self) -> None:

        while True:

            self.handle_close_event()

            pygame.display.update()


if __name__ == '__main__':

    game = Game()
    game.run()
