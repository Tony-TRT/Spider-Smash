"""
Contains everything related to the playable character.
"""

import pygame
from pathlib import Path

from modules import constants
from modules import toolkit
from modules.spiders import spider_sprites
from modules.toolkit import load_images, calculate_movement


player_sprite = pygame.sprite.GroupSingle()


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        ##############################
        # Assets.
        ##############################

        self.assets: dict = load_images(folder=Path(constants.GRAPHICS_DIR / "player"), alpha=True)

        self.idle_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("hero_idle"),
            sprites_size=16,
            sprites_number=3
        ).sprite_surfaces(2)

        self.walk_down_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("hero_walk_down"),
            sprites_size=16,
            sprites_number=4
        ).sprite_surfaces(2)

        self.walk_up_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("hero_walk_up"),
            sprites_size=16,
            sprites_number=4
        ).sprite_surfaces(2)

        self.walk_side_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("hero_walk_side"),
            sprites_size=16,
            sprites_number=4
        ).sprite_surfaces(2)

        ##############################

        self.game_surface = pygame.display.get_surface()
        self.velocity: int = 3
        self.stamina: int = 100
        self.hearts: int = 5
        self.invulnerability_time: int = 0
        self.invulnerable: bool = False
        self.dead_zone: int = 10
        self.animation_frame_delay: int = 0
        self.frame_index: int = 0

        self.image = self.idle_sprites[self.frame_index]
        self.rect = pygame.rect.Rect(434, 209, 32, 32)

    def minus_one_heart(self) -> None:

        if self.hearts and not self.invulnerable:
            self.hearts -= 1

    @property
    def now(self):

        return pygame.time.get_ticks()

    def set_invulnerable(self, duration: int) -> None:

        if not self.invulnerable:
            self.invulnerability_time = self.now + duration
            self.invulnerable = True

    def update(self):

        mov_x, mov_y = calculate_movement(pygame.mouse.get_pos(), self.rect, self.dead_zone, self.velocity)
        self.rect.move_ip(mov_x, mov_y)

        press_run = pygame.mouse.get_pressed()[2]

        if press_run and self.stamina > 0:
            self.velocity = 7
            self.stamina -= 1
        else:
            self.velocity = 3
            self.stamina = self.stamina + 0.2 if self.stamina < 100 and not press_run else self.stamina

        self.invulnerable = False if self.invulnerability_time <= self.now else self.invulnerable

        if pygame.sprite.groupcollide(player_sprite, spider_sprites, False, False):

            self.minus_one_heart()
            self.set_invulnerable(duration=1200)
