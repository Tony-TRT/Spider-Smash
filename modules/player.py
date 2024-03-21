"""
Contains everything related to the playable character.
"""

import pygame
from pathlib import Path

from modules import constants
from modules.spiders import spider_sprites
from modules.toolkit import load_images, calculate_movement


player_sprite = pygame.sprite.GroupSingle()


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.player_assets: dict = load_images(folder=Path(constants.GRAPHICS_DIR / "player"), alpha=True)
        self.hud_assets: dict = load_images(folder=Path(constants.GRAPHICS_DIR / "hud"), alpha=True)
        self.display_surface = pygame.display.get_surface()
        self.velocity: int = 3
        self.stamina: float = 100
        self.stamina_rect = None
        self.hearts: list = [pygame.rect.Rect(20 + (i * 50), 20, 20, 20) for i in range(5)]
        self.invulnerability_time: int = 0
        self.invulnerable: bool = False
        self.dead_zone: int = 10
        self.image = self.player_assets.get("sample")
        self.rect = pygame.rect.Rect(434, 209, 32, 32)

    def display_hud(self):

        self.stamina_rect = pygame.rect.Rect(670, 20, self.stamina * 2, 18)
        pygame.draw.rect(self.display_surface, (102, 255, 51), self.stamina_rect)
        self.display_surface.blit(self.hud_assets.get("stamina"), (660, 20))

        for heart in self.hearts:
            self.display_surface.blit(self.hud_assets.get("heart"), heart)

    def minus_one_heart(self) -> None:

        if self.hearts and not self.invulnerable:
            self.hearts.pop()

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
            self.set_invulnerable(duration=1500)
