import pygame
from random import randint, choice

from modules.toolkit import calculate_movement


class Spider(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.velocity: int = 2

        random_x_spawn: tuple = (randint(-100, -32), randint(932, 1000))
        random_y_spawn: tuple = (randint(-100, -32), randint(482, 550))
        xy_spawn: tuple[int: int] = (choice(random_x_spawn), choice(random_y_spawn))

        self.image = None
        self.rect = pygame.rect.Rect(*xy_spawn, 32, 32)

    def display(self):

        pygame.draw.rect(self.display_surface, (0, 255, 0), self.rect)

    def update(self, player_position: tuple[int, int]):

        mov_x, mov_y = calculate_movement(player_position, self.rect, 15, self.velocity)
        self.rect.move_ip(mov_x, mov_y)
