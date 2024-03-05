"""
The game menu is managed here.
"""

import pygame
from pathlib import Path

from modules import constants, toolkit


class GameMenu:

    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.images: dict = toolkit.load_images(folder=Path(constants.GRAPHICS_DIR / "menu"), alpha=True)
        game_font = pygame.font.Font(Path(constants.ASSETS_DIR / "font" / "font.otf"), 50)

        self.game_title = game_font.render("Spider Smash", True, (255, 255, 255))
        self.game_title_rect = self.game_title.get_rect(midbottom=(450, 0))
        self.game_title_background_rect = self.images.get("title_background").get_rect(midleft=(900, 110))
        self.game_title_frame_rect = self.images.get("title_frame").get_rect(midtop=(450, 450))
        self.game_title_light_rect = self.images.get("light").get_rect(midright=(-550, 110))
        self.background_rect = self.images.get("background").get_rect(midright=(0, 225))

    def display(self):

        self.display_surface.fill("black")
        self.display_surface.blit(self.images.get("background"), self.background_rect)
        self.display_surface.blit(self.images.get("title_background"), self.game_title_background_rect)
        self.display_surface.blit(self.game_title, self.game_title_rect)
        self.display_surface.blit(self.images.get("title_frame"), self.game_title_frame_rect)
        self.display_surface.blit(self.images.get("light"), self.game_title_light_rect)

    def update(self):

        if self.background_rect.right < 900:
            self.background_rect.right += 30

        if self.background_rect.right == 900 and self.game_title_rect.centery < 110:
            self.game_title_rect.y += 5

        if self.game_title_rect.centery == 110 and self.game_title_background_rect.left > 0:
            self.game_title_background_rect.left -= 20

        if self.game_title_background_rect.left == 0 and self.game_title_frame_rect.centery > 110:
            self.game_title_frame_rect.y -= 8

        if self.game_title_frame_rect.centery == 110:
            self.game_title_light_rect.right += 55
