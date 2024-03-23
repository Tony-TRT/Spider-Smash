"""
This module contains the Hud class, which, as the name suggests, handles the management
of the Heads-Up Display (HUD) by receiving player data to update visual indicators accordingly.
"""

import pygame
from pathlib import Path

from modules import constants
from modules import toolkit


class Hud:
    """Handles the management of the Heads-Up Display (HUD)."""

    def __init__(self):

        self.game_surface: pygame.Surface = pygame.display.get_surface()
        self.hud_surface: pygame.Surface = pygame.Surface((900, 450), pygame.SRCALPHA, 32).convert_alpha()

        self.player_hearts: int = 0
        self.heart_rectangles = None
        self.stamina_rectangle = None

        self.frame_index: int = 0
        self.animation_frame_delay: int = 0

        ##############################
        # Assets.
        ##############################

        self.assets: dict = toolkit.load_images(folder=Path(constants.GRAPHICS_DIR / "hud"), alpha=True)

        self.heart_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("animated-heart"),
            sprites_size=128,
            sprites_number=2
        ).sprite_surfaces(0.25)

    def animate_hearts(self) -> pygame.Surface:
        """This method manages the animation of the hearts shown on the HUD, cycling through the frames
        of the heart animation at a specified delay. It updates the current frame index and returns
        the corresponding heart image to be displayed. If the animation frame delay has elapsed,
        it advances to the next frame; otherwise, it maintains the current frame.

        Returns:
            pygame.Surface: The current frame of the heart animation.
        """

        if self.animation_frame_delay <= 0:

            self.animation_frame_delay = 15
            self.frame_index = (self.frame_index + 1) % len(self.heart_sprites)

        return self.heart_sprites[self.frame_index]

    def update(self, player_hearts: int, player_stamina: int) -> None:

        self.hud_surface.fill((0, 0, 0, 0))

        # Update the variables.
        self.player_hearts = player_hearts
        self.heart_rectangles = [pygame.rect.Rect(20 + (i * 50), 20, 20, 20) for i in range(self.player_hearts)]
        self.stamina_rectangle = pygame.rect.Rect(670, 20, player_stamina * 2, 18)
        self.animation_frame_delay -= 1

        # Display the stamina bar.
        pygame.draw.rect(self.hud_surface, (255, 10, 10), self.stamina_rectangle)
        self.hud_surface.blit(self.assets.get("stamina"), (660, 20))

        # Display and update the hearts.
        for heart in self.heart_rectangles:

            self.hud_surface.blit(self.animate_hearts(), heart)

        self.game_surface.blit(self.hud_surface, (0, 0))
