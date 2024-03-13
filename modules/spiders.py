import pygame
from random import randint, choice
from pathlib import Path

from modules import constants
from modules.toolkit import calculate_movement, load_images


spider_sprites = pygame.sprite.Group()


class Spider(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.velocity: int = 2

        random_x_spawn: tuple[int, int] = (randint(-100, -32), randint(932, 1000))
        random_y_spawn: tuple[int, int] = (randint(-100, -32), randint(482, 550))
        xy_spawn: tuple[int: int] = (choice(random_x_spawn), choice(random_y_spawn))

        self.images: dict = load_images(folder=Path(constants.GRAPHICS_DIR / "spiders"), alpha=True)
        self.image = self.images.get("sample")
        self.rect = pygame.rect.Rect(*xy_spawn, 32, 32)

    def update(self, player_position: tuple[int, int]):

        mov_x, mov_y = calculate_movement(player_position, self.rect, 15, self.velocity)
        self.rect.move_ip(mov_x, mov_y)
