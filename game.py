"""
This module serves as the core module of the game, containing essential elements such as the Game class.
"""

import sys
import pygame
from pathlib import Path

from modules import constants
from modules.menu import GameMenu
from modules.hud import Hud
from modules.player import Player, player_sprite, player_blood_effects
from modules.spiders import AdultSpider, spider_sprites, spider_blood_effects
from modules.weapons import Bullet, bullet_sprites
from modules.toolkit import GameState, load_images, detect_collision


class Game:

    def __init__(self):

        ##############################
        # Basic required code.
        ##############################

        pygame.init()
        pygame.mixer.init()

        self.display_surface = pygame.display.set_mode((900, 450))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Spider Smash")

        ##############################
        # Useful variables.
        ##############################

        self.assets: dict = load_images(folder=Path(constants.GRAPHICS_DIR / "general"))
        self.game_music = pygame.mixer.Sound(Path(constants.AUDIO_DIR / "general" / "game_music.ogg"))
        self.game_music.set_volume(0.2)
        self.do_game_music: bool = True
        self.game_over_music = pygame.mixer.Sound(Path(constants.AUDIO_DIR / "general" / "game_over.wav"))
        self.do_game_over_music: bool = True
        self.game_menu_music = pygame.mixer.Sound(Path(constants.AUDIO_DIR / "menu" / "game_menu.ogg"))
        self.game_menu_music.set_volume(0.2)
        self.do_game_menu_music: bool = True
        self.start_sound = pygame.mixer.Sound(Path(constants.AUDIO_DIR / "menu" / "start.wav"))
        self.start_sound.set_volume(0.35)
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
        self.event_score_second = pygame.USEREVENT + 2
        self.event_score_minute = pygame.USEREVENT + 3

        pygame.time.set_timer(self.event_spider_spawn, 350)
        pygame.time.set_timer(self.event_score_second, 1000)
        pygame.time.set_timer(self.event_score_minute, 60000)

    def display_menu(self) -> None:

        if self.do_game_menu_music:

            self.game_menu_music.play(-1)
            self.do_game_menu_music = False

        self.menu.display()
        self.menu.update()

    def do_game(self) -> None:

        if self.do_game_music:

            self.game_music.play(-1)
            self.do_game_music = False

        self.display_surface.blit(self.assets.get("ground"), (0, 0))

        if self.keys[pygame.K_SPACE]:

            position: tuple[int, int] = (int(self.player.rect.centerx), int(self.player.rect.centery))
            bullet: Bullet = Bullet(player_position=position, player_direction=self.player.direction[0])
            bullet_sprites.add(bullet)

        spider_blood_effects.draw(self.display_surface)
        player_blood_effects.draw(self.display_surface)

        for spider in spider_sprites:

            spider.draw_shadow()

        self.player.draw_shadow()

        spider_sprites.draw(self.display_surface)
        bullet_sprites.draw(self.display_surface)
        player_sprite.draw(self.display_surface)

        spider_blood_effects.update()
        player_blood_effects.update()
        spider_sprites.update(self.player.rect.center)
        bullet_sprites.update()
        player_sprite.update()

        self.hud.update(self.player.hearts, self.player.stamina)

        if detect_collision(bullet_sprites, spider_sprites, True, True):
            self.hud.player_score += 5

        self.state = GameState.OVER if not self.player.hearts else self.state

    def do_game_over(self) -> None:

        self.game_music.stop()

        if self.do_game_over_music:

            self.game_over_music.play()
            self.do_game_over_music = False

        self.display_surface.fill((0, 0, 0))

    def do_menu(self) -> None:

        self.display_menu()

        if self.keys[pygame.K_SPACE]:

            self.game_menu_music.stop()
            self.start_sound.play()
            self.state = GameState.ACTIVE

    def handle_events(self) -> None:

        events: list = [event.type for event in pygame.event.get()]

        if pygame.QUIT in events:
            pygame.quit()
            sys.exit()

        if self.event_spider_spawn in events and self.state == GameState.ACTIVE:
            spider_sprites.add(AdultSpider())

        if self.event_score_second in events and self.state == GameState.ACTIVE:
            self.hud.player_score += 1

        if self.event_score_minute in events and self.state == GameState.ACTIVE:
            self.hud.player_score += 100

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
