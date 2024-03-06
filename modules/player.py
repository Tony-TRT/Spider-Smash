"""
Contains everything related to the playable character.
"""

import pygame
from pathlib import Path

from modules import constants
from modules.toolkit import load_images


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.velocity: int = 3
        self.dead_zone: int = 10
        self.images: dict = load_images(folder=Path(constants.GRAPHICS_DIR / "player"), alpha=True)
        self.image = None
        self.rect = pygame.rect.Rect(434, 209, 32, 32)

    def display(self):

        pygame.draw.rect(self.display_surface, (255, 255, 255), self.rect)

    def update(self):

        # Get the current position of the mouse cursor.
        mouse_pos = pygame.mouse.get_pos()

        # Calculate the horizontal and vertical differences
        # between the mouse position and the center of the rectangle.
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery

        # Calculate the distance between the mouse cursor and
        # the center of the rectangle using the Pythagorean theorem.
        distance: float = ((dx ** 2) + (dy ** 2)) ** 0.5

        # Check if the distance is greater than the dead zone threshold.
        if distance > self.dead_zone:
            mov_x = dx / distance * self.velocity
            mov_y = dy / distance * self.velocity

            # Move the rectangle in place by the calculated horizontal and vertical movements.
            self.rect.move_ip(mov_x, mov_y)
