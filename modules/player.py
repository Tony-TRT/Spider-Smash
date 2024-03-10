"""
Contains everything related to the playable character.
"""

import pygame
from pathlib import Path

from modules import constants
from modules.toolkit import load_images, calculate_movement


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.velocity: int = 3
        self.stamina: float = 100
        self.stamina_rect = None
        self.hearts: list = [pygame.rect.Rect(20 + (i * 40), 20, 20, 20) for i in range(5)]
        self.dead_zone: int = 10
        self.images: dict = load_images(folder=Path(constants.GRAPHICS_DIR / "player"), alpha=True)
        self.image = None
        self.rect = pygame.rect.Rect(434, 209, 32, 32)

    def display(self):

        self.stamina_rect = pygame.rect.Rect(680, 20, self.stamina * 2, 20)

        pygame.draw.rect(self.display_surface, (255, 255, 255), self.rect)
        pygame.draw.rect(self.display_surface, (0, 0, 255), self.stamina_rect)

        for heart in self.hearts:
            pygame.draw.rect(self.display_surface, (255, 0, 0), heart)

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
