import pygame
from math import atan2, cos, sin
from pathlib import Path

from modules import constants


bullet_sprites = pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet fired by the player.
    """

    def __init__(self, player_pos: tuple):
        super().__init__()

        image = pygame.image.load(Path(constants.GRAPHICS_DIR / "weapons" / "fireball.png"))
        image.set_colorkey((0, 0, 0))

        self.initial_mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        self.spawn_position: tuple[int, int] = (player_pos[0] - 8, player_pos[1] - 8)

        self.display_surface = pygame.display.get_surface()
        self.speed: int = 20
        self.image = image
        self.rect = pygame.rect.Rect(*self.spawn_position, 5, 5)

        distance_x = self.initial_mouse_pos[0] - self.spawn_position[0]
        distance_y = self.initial_mouse_pos[1] - self.spawn_position[1]
        angle: float = atan2(distance_y, distance_x)

        self.speed_x = self.speed * cos(angle)
        self.speed_y = self.speed * sin(angle)
        self.bullet_repr: list = [
            self.spawn_position[0],
            self.spawn_position[1],
            self.speed_x,
            self.speed_y
        ]

    def update(self):

        self.bullet_repr[0] += self.bullet_repr[2]
        self.bullet_repr[1] += self.bullet_repr[3]

        pos_x, pos_y = self.bullet_repr[:2]
        self.rect.center = (int(pos_x), int(pos_y))

        if not (-5 <= self.rect.centerx <= 905) or not (-5 <= self.rect.centery <= 455):
            self.kill()
