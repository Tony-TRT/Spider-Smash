"""
This module contains useful elements that can be used several times.
"""

import pygame
from pathlib import Path


def load_images(folder: Path, alpha: bool = False) -> dict:

    return {
        image.stem: pygame.image.load(image).convert_alpha() if alpha else pygame.image.load(image).convert()
        for image in folder.iterdir() if image.is_file()
    }
