"""
The game menu is managed here.
"""

import pygame
from pathlib import Path

from modules import constants, toolkit


class GameMenu:

    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.images: dict = toolkit.load_images(Path(constants.GRAPHICS_DIR / "menu"))
        self.font = pygame.font.Font(Path(constants.ASSETS_DIR / "font" / "font.otf"), 50)

    def display(self):

        self.display_surface.blit(self.images.get("background"), (0, 0))

    def update(self):

        pass
