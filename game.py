"""
This module serves as the core module of the game, containing essential elements such as the Game class.
"""

import sys
import pygame
from pathlib import Path

from modules import constants
from modules.menu import GameMenu
from modules.hud import Hud
from modules.player import Player, player_sprite
from modules.spiders import AdultSpider, spider_sprites, spider_blood_effects
from modules.weapons import Bullet, bullet_sprites
from modules.toolkit import GameState, load_images


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

        self.assets: dict = load_images(folder=Path(constants.GRAPHICS_DIR / "general"))
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
        self.hud = Hud()

        player_sprite.add(self.player)

        ##############################
        # Events.
        ##############################

        self.event_spider_spawn = pygame.USEREVENT + 1

        pygame.time.set_timer(self.event_spider_spawn, 400)

    def display_menu(self) -> None:

        self.menu.display()
        self.menu.update()

    def do_game(self) -> None:

        self.display_surface.blit(self.assets.get("ground"), (0, 0))

        if self.keys[pygame.K_SPACE]:
            bullet_sprites.add(Bullet((int(self.player.rect.centerx), int(self.player.rect.centery))))

        spider_blood_effects.draw(self.display_surface)
        spider_sprites.draw(self.display_surface)
        player_sprite.draw(self.display_surface)
        bullet_sprites.draw(self.display_surface)

        spider_blood_effects.update()
        spider_sprites.update(self.player.rect.center)
        player_sprite.update()
        bullet_sprites.update()

        self.hud.update(self.player.hearts, self.player.stamina)

        pygame.sprite.groupcollide(bullet_sprites, spider_sprites, True, True)

        self.state = GameState.OVER if not self.player.hearts else self.state

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
            spider_sprites.add(AdultSpider())

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
