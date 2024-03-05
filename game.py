"""
This module serves as the core module of the game, containing essential elements such as the Game class.
"""

import sys
import pygame

from modules.menu import GameMenu


class Game:

    def __init__(self):

        pygame.init()
        self.game_over: bool = False
        self.active_menu: bool = True
        self.game_menu = GameMenu()
        self.display_surface = pygame.display.set_mode((900, 450))
        pygame.display.set_caption("Spider Smash")

    def display_menu(self):

        self.game_menu.display()
        self.game_menu.update()

    @staticmethod
    def handle_close_event() -> None:

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def run(self) -> None:

        while True:

            self.handle_close_event()

            if self.game_over:

                pass
                # Game Over

            elif self.active_menu:

                self.display_menu()

            else:

                pass
                # Game

            pygame.display.update()


if __name__ == '__main__':

    game = Game()
    game.run()
