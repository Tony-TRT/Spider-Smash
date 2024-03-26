"""
This module contains useful elements that can be used several times.
"""

import pygame
from pygame.sprite import collide_mask, AbstractGroup
from pygame.rect import Rect
from pathlib import Path
from math import sqrt
from enum import Enum, auto


class SpritesLoader:

    def __init__(self, sprites_image: pygame.Surface, sprites_size: int, sprites_number: int):

        self.main_image = sprites_image
        self.sprites_size: int = sprites_size
        self.sprites_number: int = sprites_number

    def _get_sprite(self, frame_index: int, scale_factor: float = 1) -> pygame.Surface:
        """Generates a surface for a specific sprite frame.

        Args:
            frame_index (int): The index of the sprite frame to retrieve.
            scale_factor (float, optional): The factor by which to scale the sprite surface.

        Returns:
            pygame.Surface: The surface containing the specified sprite frame.
        """

        surface = pygame.Surface((self.sprites_size, self.sprites_size), pygame.SRCALPHA)
        source_area = (frame_index * self.sprites_size, 0, self.sprites_size, self.sprites_size)
        surface.blit(source=self.main_image, dest=(0, 0), area=source_area)
        size = (self.sprites_size * scale_factor, self.sprites_size * scale_factor)
        return pygame.transform.scale(surface=surface, size=size)

    def sprite_surfaces(self, scale_factor: float = 1) -> list[pygame.Surface]:
        """Generates surfaces for all sprite frames.

        Args:
            scale_factor (float, optional): The factor by which to scale the sprite surfaces.

        Returns:
            list[pygame.Surface]: A list containing surfaces for all sprite frames.
        """

        return [self._get_sprite(i, scale_factor=scale_factor) for i in range(self.sprites_number)]


class GameState(Enum):
    """
    Enumeration representing different states of the game.
    """

    ACTIVE = auto()
    MENU = auto()
    OVER = auto()


class Direction(Enum):
    """
    Enum class representing cardinal and ordinal directions.
    """

    NORTHWEST = 45
    NORTH = 0
    NORTHEAST = 315
    EAST = 270
    SOUTHEAST = 225
    SOUTH = 180
    SOUTHWEST = 135
    WEST = 90
    NONE = 0


def detect_collision(group_a: AbstractGroup, group_b: AbstractGroup, kill_a: bool, kill_b: bool) -> bool:

    if not pygame.sprite.groupcollide(group_a, group_b, False, False):

        return False

    if pygame.sprite.groupcollide(group_a, group_b, kill_a, kill_b, collide_mask):  # type: ignore

        return True


def get_direction(dx, dy, margin: int = 60) -> Direction:
    """Determine the direction of movement based on horizontal and vertical components.

    Args:
        dx (int): The horizontal component of the movement.
        dy (int): The vertical component of the movement.
        margin (int, optional): The margin of error to consider for horizontal and vertical movements.

    Returns:
        Direction: The direction of movement as an instance of Direction enum.
    """

    # Check if the absolute value of dy is less than the margin.
    # If dy is within the margin, it indicates horizontal movement.
    if abs(dy) < margin:

        # Check the sign of dx to determine the direction
        if dx < 0:
            return Direction.WEST
        elif dx > 0:
            return Direction.EAST

    # If dy is not within the margin, check if dx is within the margin.
    # If dx is within the margin, it indicates vertical movement.
    elif abs(dx) < margin:

        # Check the sign of dy to determine the direction.
        if dy < 0:
            return Direction.NORTH
        elif dy > 0:
            return Direction.SOUTH

    # If neither dx nor dy are within the margin, consider diagonal movement.
    else:
        # Check the signs of dx and dy to determine the diagonal direction.
        if dy < 0:
            # If dy is negative, the movement is towards the top.
            return Direction.NORTHWEST if dx < 0 else Direction.NORTHEAST
        elif dy > 0:
            # If dy is positive, the movement is towards the bottom.
            return Direction.SOUTHWEST if dx < 0 else Direction.SOUTHEAST

    # If none of the above conditions are met.
    return Direction.NONE


def get_shadow_surface(surface: pygame.Surface) -> pygame.Surface:

    shadow_surface: pygame.Surface = surface.copy()
    black_surface: pygame.Surface = pygame.Surface(shadow_surface.get_size(), pygame.SRCALPHA)
    black_surface.fill((0, 0, 0, 150))
    shadow_surface.blit(black_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return shadow_surface


def load_images(folder: Path, alpha: bool = False) -> dict:
    """Load images from a specified folder.

    Args:
        folder (Path): The path to the folder containing the images.
        alpha (bool, optional): Whether to load images with alpha transparency. Defaults to False.

    Returns:
        dict: A dictionary where keys are the filenames (without extension) of the images
        and values are the corresponding pygame.Surface objects representing the loaded images.
    """

    return {
        image.stem: pygame.image.load(image).convert_alpha() if alpha else pygame.image.load(image).convert()
        for image in folder.iterdir() if image.is_file()
    }


def calculate_movement(destination: tuple[int, int], rect: Rect, dead_zone: int, velocity: int) -> tuple[float, float]:
    """Calculate the movement required to reach a destination point.

    Args:
        destination (tuple[int, int]): The target coordinates (x, y) to move towards.
        rect (Rect): The rectangle representing the current position and size of the object.
        dead_zone (int): The radius within which no movement is necessary.
        velocity (int): The speed at which the object should move.

    Returns:
        tuple[float, float]: A tuple containing the horizontal and vertical movement
        required to reach the destination point. If the distance to the destination is within
        the dead zone, returns (0, 0).
    """

    # Calculate the horizontal and vertical differences
    # between the destination position and the center of the rectangle.
    dx = destination[0] - rect.centerx
    dy = destination[1] - rect.centery

    # Calculate the distance between the destination and
    # the center of the rectangle using the Pythagorean theorem.
    distance: float = sqrt((dx ** 2) + (dy ** 2))

    # Check if the distance is greater than the dead zone threshold.
    if distance > dead_zone:
        return dx / distance * velocity, dy / distance * velocity
    return 0, 0
