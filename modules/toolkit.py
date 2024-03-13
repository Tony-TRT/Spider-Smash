"""
This module contains useful elements that can be used several times.
"""

import pygame
from pygame.rect import Rect
from pathlib import Path
from math import sqrt
from enum import Enum, auto


class GameState(Enum):
    """
    Enumeration representing different states of the game.
    """

    ACTIVE = auto()
    MENU = auto()
    OVER = auto()


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
