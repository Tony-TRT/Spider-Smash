"""
This module serves as the core module of the game, containing essential elements such as the Game class.
"""

import sys
import pygame

from modules.menu import GameMenu
from modules.player import Player
from modules.spiders import Spider


class Game:

    def __init__(self):

        pygame.init()
        self.game_over: bool = False
        self.active_menu: bool = True
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((900, 450))
        self.game_menu = GameMenu()
        self.player = Player()
        self.spiders: list = []
        pygame.display.set_caption("Spider Smash")

    def display_menu(self):

        self.game_menu.display()
        self.game_menu.update()

    def run(self) -> None:

        spider_spawn = pygame.USEREVENT + 1
        pygame.time.set_timer(spider_spawn, 500)

        while True:

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == spider_spawn and not self.active_menu and not self.game_over:
                    self.spiders.append(Spider())

            if self.game_over:

                pass
                # Game Over

            elif self.active_menu:  # Menu.

                self.display_menu()
                if keys[pygame.K_SPACE]:
                    self.active_menu = False

            else:  # Game.

                self.display_surface.fill("black")

                for spider in self.spiders:

                    spider.display()
                    spider.update(self.player.rect.center)

                self.player.display()
                self.player.update()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':

    game = Game()
    game.run()
