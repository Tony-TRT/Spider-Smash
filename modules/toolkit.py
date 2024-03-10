"""
This module contains useful elements that can be used several times.
"""

import pygame
from pygame.rect import Rect
from pathlib import Path
from math import sqrt


def load_images(folder: Path, alpha: bool = False) -> dict:

    return {
        image.stem: pygame.image.load(image).convert_alpha() if alpha else pygame.image.load(image).convert()
        for image in folder.iterdir() if image.is_file()
    }


def calculate_movement(destination: tuple[int, int], rect: Rect, dead_zone: int, velocity: int) -> tuple[float, float]:

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
