"""
This module serves as the core module of the game, containing essential elements such as the Game class.
"""

import sys
import pygame

from modules.menu import GameMenu
from modules.player import Player, player_sprite
from modules.spiders import Spider, spider_sprites
from modules.weapons import Bullet, bullet_sprites
from modules.toolkit import GameState


class Game:

    def __init__(self):

        ##############################
        # Basic required code.
        ##############################

        pygame.init()

        self.display_surface = pygame.display.set_mode((900, 450))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Spider Smash")

        ##############################
        # Useful variables.
        ##############################

        self.state = GameState.MENU
        self.game_state_action: dict = {
            GameState.ACTIVE: self.do_game,
            GameState.MENU: self.do_menu,
            GameState.OVER: self.do_game_over
        }

        ##############################
        # Game elements.
        ##############################

        self.player = Player()
        self.menu = GameMenu()

        player_sprite.add(self.player)

        ##############################
        # Events.
        ##############################

        self.event_spider_spawn = pygame.USEREVENT + 1

        pygame.time.set_timer(self.event_spider_spawn, 500)

    def display_menu(self) -> None:

        self.menu.display()
        self.menu.update()

    def do_game(self) -> None:

        self.display_surface.fill((0, 0, 0))

        if self.keys[pygame.K_SPACE]:
            bullet_sprites.add(Bullet(self.player.rect.center))

        spider_sprites.draw(self.display_surface)
        player_sprite.draw(self.display_surface)
        bullet_sprites.draw(self.display_surface)

        spider_sprites.update(self.player.rect.center)
        player_sprite.update()
        bullet_sprites.update()

        self.player.display_hud()

        pygame.sprite.groupcollide(bullet_sprites, spider_sprites, True, True)

        if pygame.sprite.groupcollide(player_sprite, spider_sprites, False, False):
            try:
                self.player.hearts.pop()
            except IndexError:
                self.state = GameState.OVER

    def do_game_over(self) -> None:

        self.display_surface.fill((0, 0, 0))

    def do_menu(self) -> None:

        self.display_menu()

        if self.keys[pygame.K_SPACE]:
            self.state = GameState.ACTIVE

    def handle_events(self) -> None:

        events: list = [event.type for event in pygame.event.get()]

        if pygame.QUIT in events:
            pygame.quit()
            sys.exit()

        if self.event_spider_spawn in events and self.state == GameState.ACTIVE:
            spider_sprites.add(Spider())

    @property
    def keys(self):

        return pygame.key.get_pressed()

    def run(self) -> None:

        while True:

            self.handle_events()
            self.game_state_action[self.state]()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':

    game = Game()
    game.run()
