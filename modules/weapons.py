import pygame
from math import atan2, cos, sin


class Bullet(pygame.sprite.Sprite):

    def __init__(self, player_pos: tuple):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.speed: int = 20
        self.image = None
        self.rect = pygame.rect.Rect(*player_pos, 5, 5)

        self.initial_mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        self.initial_player_pos: tuple = player_pos
        distance_x = self.initial_mouse_pos[0] - self.initial_player_pos[0]
        distance_y = self.initial_mouse_pos[1] - self.initial_player_pos[1]
        angle: float = atan2(distance_y, distance_x)

        self.speed_x = self.speed * cos(angle)
        self.speed_y = self.speed * sin(angle)
        self.bullet_repr: list = [
            self.initial_player_pos[0],
            self.initial_player_pos[1],
            self.speed_x,
            self.speed_y
        ]

    def display(self):

        pygame.draw.circle(self.display_surface, (255, 0, 0), self.rect.center, 8)

    def update(self):

        self.bullet_repr[0] += self.bullet_repr[2]
        self.bullet_repr[1] += self.bullet_repr[3]

        pos_x, pos_y = self.bullet_repr[:2]
        self.rect.center = (int(pos_x), int(pos_y))
