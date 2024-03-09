import pygame
from random import randint, choice


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

    def update(self, player_x_pos, player_y_pos):

        dx = player_x_pos - self.rect.centerx
        dy = player_y_pos - self.rect.centery

        distance: float = ((dx ** 2) + (dy ** 2)) ** 0.5

        if distance > 0:
            mov_x = dx / distance * self.velocity
            mov_y = dy / distance * self.velocity

            self.rect.move_ip(mov_x, mov_y)
