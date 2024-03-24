"""
This module contains functionality related to weapons.
"""

import pygame
from math import atan2, cos, sin
from pathlib import Path
from random import randint

from modules import constants


bullet_sprites = pygame.sprite.Group()
bullet_image: pygame.Surface = pygame.image.load(Path(constants.GRAPHICS_DIR / "weapons" / "fireball.png"))
bullet_image.set_colorkey((0, 0, 0))


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet fired by the player.
    """

    def __init__(self, player_position: tuple[int, int]):
        super().__init__()

        self.game_surface: pygame.Surface = pygame.display.get_surface()
        self.light_surface: pygame.Surface = pygame.Surface((900, 450), pygame.SRCALPHA)

        ##############################

        self.initial_mouse_position: tuple[int, int] = pygame.mouse.get_pos()
        self.spawn_position: tuple[int, int] = (player_position[0] - 8, player_position[1] - 8)
        self.speed: int = 20

        ##############################

        self.image = bullet_image
        self.rect = pygame.rect.Rect(*self.spawn_position, 5, 5)

        ##############################

        self.speed_x = self.speed * cos(self.angle)
        self.speed_y = self.speed * sin(self.angle)

        self.bullet_repr: list = [
            self.spawn_position[0],
            self.spawn_position[1],
            self.speed_x,
            self.speed_y
        ]

    @property
    def angle(self) -> float:
        """Calculates the angle (in radians) between the bullet's spawn position
        and the initial mouse position.

        Returns:
            float: The angle in radians.
        """

        distance_x = self.initial_mouse_position[0] - self.spawn_position[0]
        distance_y = self.initial_mouse_position[1] - self.spawn_position[1]

        return atan2(distance_y, distance_x)

    def render_light_effect(self) -> None:
        """Renders a light effect around the bullet's position on a separate surface.

        This method fills the light surface with a transparent color and draws
        a semi-transparent circle representing the light effect around the
        bullet's current position.
        """

        self.light_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(
            surface=self.light_surface,
            color=(255, 153, 0, 7),
            center=self.rect.center,
            radius=randint(a=35, b=50),
            width=0
        )

    def update_position(self) -> None:
        """Updates the position of the bullet on the screen.

        This method adjusts the position of the bullet based on its current velocity
        (stored in the bullet_repr attribute). It also updates the position of the
        bullet's sprite rectangle to match its new position. If the bullet moves
        outside the screen boundaries, it is removed from the sprite group.
        """

        self.bullet_repr[0] += self.bullet_repr[2]
        self.bullet_repr[1] += self.bullet_repr[3]

        pos_x, pos_y = self.bullet_repr[:2]
        self.rect.center = (int(pos_x), int(pos_y))

        if not (-5 <= self.rect.centerx <= 905) or not (-5 <= self.rect.centery <= 455):
            self.kill()

    def update(self) -> None:

        self.update_position()
        self.render_light_effect()
        self.game_surface.blit(self.light_surface, (0, 0))
