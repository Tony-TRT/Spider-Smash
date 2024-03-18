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
        self.text_direction: bool = True
        game_font_big = pygame.font.Font(Path(constants.ASSETS_DIR / "font" / "font.otf"), 50)
        game_font_small = pygame.font.Font(Path(constants.ASSETS_DIR / "font" / "font.otf"), 25)

        self.game_title = game_font_big.render("Spider Smash", True, (255, 255, 255))
        self.game_title_rect = self.game_title.get_rect(midbottom=(450, 0))
        self.game_title_background_rect = self.images.get("title_background").get_rect(midleft=(900, 110))
        self.game_title_frame_rect = self.images.get("title_frame").get_rect(midtop=(450, 450))
        self.game_title_light_rect = self.images.get("light").get_rect(midright=(-550, 110))
        self.background_rect = self.images.get("background").get_rect(midright=(0, 225))
        self.menu_text = game_font_small.render("Press SPACE to play", True, (0, 0, 0))
        self.menu_text_outline = game_font_small.render("Press SPACE to play", True, (255, 255, 255))
        self.menu_text_rect = self.menu_text.get_rect(center=(450, 380))
        self.menu_text_outline_rect = self.menu_text_outline.get_rect(center=(453, 377))

    def animate_light(self):

        self.game_title_light_rect.right += 55

        if self.game_title_light_rect.left >= 900:
            self.game_title_light_rect.right = -30000

    def animate_menu_text(self):

        speed = 2
        self.menu_text_rect.x += speed if self.text_direction else -speed
        self.menu_text_outline_rect.x += speed if self.text_direction else -speed

        if self.menu_text_rect.right >= 900 or self.menu_text_rect.left <= 0:
            self.text_direction = not self.text_direction

    def display(self):

        self.display_surface.fill((0, 0, 0))
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

        if self.game_title_frame_rect.centery == 110 and self.game_title_light_rect.left < 900:
            self.animate_light()

        if self.game_title_background_rect.left == 0 and self.game_title_frame_rect.centery == 110:
            self.display_surface.blit(self.menu_text, self.menu_text_rect)
            self.display_surface.blit(self.menu_text_outline, self.menu_text_outline_rect)
            self.animate_menu_text()
