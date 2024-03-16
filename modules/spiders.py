import pygame
from random import randint, choice
from pathlib import Path

from modules import constants
from modules.toolkit import calculate_movement, load_images


spider_sprites = pygame.sprite.Group()


def randomize_spawn_location() -> tuple[int, int]:

    random_x_spawn: tuple[int, int] = (randint(-100, -32), randint(932, 1000))
    random_y_spawn: tuple[int, int] = (randint(-100, -32), randint(482, 550))
    return choice(random_x_spawn), choice(random_y_spawn)


class Spider(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.velocity = None
        self.spawn_position = None
        self.assets: dict = load_images(folder=Path(constants.GRAPHICS_DIR / "spiders"), alpha=True)

        self.image = None
        self.rect = None

    def update(self, player_position: tuple[int, int]):

        mov_x, mov_y = calculate_movement(player_position, self.rect, 15, self.velocity)
        self.rect.move_ip(mov_x, mov_y)


class AdultSpider(Spider):

    def __init__(self):
        super().__init__()

        self.velocity: int = 2
        self.spawn_position: tuple[int, int] = randomize_spawn_location()

        self.image = self.assets.get("sample")
        self.rect = pygame.rect.Rect(*self.spawn_position, 32, 32)

    def kill(self):
        
        if not choice(range(8)):
            self.spawn_babies()
        
        super().kill()

    def spawn_babies(self):

        for i in range(randint(a=1, b=5)):
            spider_sprites.add(BabySpider(self.rect.center))  # type: ignore


class BabySpider(Spider):

    def __init__(self, spawn_position: tuple[int, int]):
        super().__init__()

        self.velocity: int = 3
        self.spawn_position: tuple[int, int] = spawn_position

        self.image = self.assets.get("b_sample")
        self.rect = pygame.rect.Rect(*self.spawn_position, 24, 24)
