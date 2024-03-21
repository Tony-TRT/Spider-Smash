"""
This module contains everything related to spiders.
"""

import pygame
from random import randint
from pathlib import Path

from modules import constants
from modules import toolkit


spider_sprites = pygame.sprite.Group()


def randomize_spawn_location() -> tuple[int, int]:
    """Generate a random spawn location for a spider.

    Returns:
        tuple[int, int]: A tuple containing the randomly generated x and y coordinates.
    """

    random_x_spawn: int = randint(-100, 1000)
    random_y_spawn: int = randint(-100, 550)

    if not (-32 <= random_x_spawn <= 982) or not (-32 <= random_y_spawn <= 582):
        return random_x_spawn, random_y_spawn
    return randomize_spawn_location()


class Spider(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.velocity = None
        self.spawn_position = None
        self.assets: dict = toolkit.load_images(folder=Path(constants.GRAPHICS_DIR / "spiders"), alpha=True)

        self.image = None
        self.rect = None

    def update(self, player_position: tuple[int, int]):

        mov_x, mov_y = toolkit.calculate_movement(player_position, self.rect, 15, self.velocity)
        self.rect.move_ip(mov_x, mov_y)


class AdultSpider(Spider):

    def __init__(self):
        super().__init__()

        self.velocity: int = 2
        self.spawn_position: tuple[int, int] = randomize_spawn_location()
        self.idle_animation_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("idle_green_spiders"),
            sprites_size=64,
            sprites_number=7
        ).sprite_surfaces()
        self.current_frame_index: int = 0
        self.animation_frame_delay: int = 5

        self.image = self.idle_animation_sprites[self.current_frame_index]
        self.rect = pygame.rect.Rect(*self.spawn_position, 32, 32)

    def kill(self):

        if not randint(a=0, b=7):  # 1 in 8 chance to lay eggs.
            self.spawn_babies()

        super().kill()

    def spawn_babies(self):

        for _ in range(randint(a=1, b=5)):
            spider_sprites.add(BabySpider(self.rect.center))  # type: ignore

    def update(self, player_position: tuple[int, int]):

        super().update(player_position)

        dx: int = int(player_position[0] - self.rect.centerx)
        dy: int = int(player_position[1] - self.rect.centery)
        direction: toolkit.Direction = toolkit.get_direction(dx=dx, dy=dy)
        self.animation_frame_delay -= 1

        if self.animation_frame_delay <= 0:

            self.animation_frame_delay = 5
            self.current_frame_index = (self.current_frame_index + 1) % len(self.idle_animation_sprites)
            image = pygame.transform.rotate(self.idle_animation_sprites[self.current_frame_index], direction.value)
            self.image = image


class BabySpider(Spider):

    def __init__(self, spawn_position: tuple[int, int]):
        super().__init__()

        self.velocity: int = 3
        self.spawn_position: tuple[int, int] = spawn_position

        self.image = self.assets.get("b_sample")
        self.rect = pygame.rect.Rect(*self.spawn_position, 24, 24)
