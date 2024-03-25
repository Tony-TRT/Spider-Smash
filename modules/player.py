"""
Contains everything related to the playable character.
"""

import pygame
from pathlib import Path

from modules import constants
from modules import toolkit
from modules.toolkit import Direction as Drc
from modules.spiders import spider_sprites


player_sprite = pygame.sprite.GroupSingle()


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        ##############################
        # Assets.
        ##############################

        self.assets: dict = toolkit.load_images(folder=Path(constants.GRAPHICS_DIR / "player"), alpha=True)

        self.front_idle_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("front_hero_idle"),
            sprites_size=64,
            sprites_number=8
        ).sprite_surfaces()

        self.back_idle_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("back_hero_idle"),
            sprites_size=64,
            sprites_number=8
        ).sprite_surfaces()

        self.left_idle_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("left_hero_idle"),
            sprites_size=64,
            sprites_number=8
        ).sprite_surfaces()

        self.right_idle_sprites: list[pygame.Surface] = [
            pygame.transform.flip(surface, True, False) for surface in self.left_idle_sprites
        ]

        self.front_run_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("front_hero_run"),
            sprites_size=64,
            sprites_number=8
        ).sprite_surfaces()

        self.back_run_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("back_hero_run"),
            sprites_size=64,
            sprites_number=8
        ).sprite_surfaces()

        self.left_run_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("left_hero_run"),
            sprites_size=64,
            sprites_number=8
        ).sprite_surfaces()

        self.right_run_sprites: list[pygame.Surface] = [
            pygame.transform.flip(surface, True, False) for surface in self.left_run_sprites
        ]

        self.front_walk_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("front_hero_walk"),
            sprites_size=64,
            sprites_number=8
        ).sprite_surfaces()

        self.back_walk_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("back_hero_walk"),
            sprites_size=64,
            sprites_number=8
        ).sprite_surfaces()

        self.left_walk_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("left_hero_walk"),
            sprites_size=64,
            sprites_number=8
        ).sprite_surfaces()

        self.right_walk_sprites: list[pygame.Surface] = [
            pygame.transform.flip(surface, True, False) for surface in self.left_walk_sprites
        ]

        ##############################

        self.idle_direction_dict: dict = {
            Drc.NORTH: self.back_idle_sprites,
            Drc.SOUTH: self.front_idle_sprites,
            Drc.EAST: self.right_idle_sprites,
            Drc.WEST: self.left_idle_sprites
        }

        self.walk_direction_dict: dict = {
            Drc.NORTH: self.back_walk_sprites,
            Drc.SOUTH: self.front_walk_sprites,
            Drc.EAST: self.right_walk_sprites,
            Drc.WEST: self.left_walk_sprites
        }

        self.run_direction_dict: dict = {
            Drc.NORTH: self.back_run_sprites,
            Drc.SOUTH: self.front_run_sprites,
            Drc.EAST: self.right_run_sprites,
            Drc.WEST: self.left_run_sprites
        }

        ##############################

        self.game_surface = pygame.display.get_surface()
        self.velocity: int = 3
        self.stamina: int = 100
        self.hearts: int = 5
        self.invulnerability_time: int = 0
        self.invulnerable: bool = False
        self.dead_zone: int = 10
        self.animation_frame_delay: int = 0
        self.idle_frame_index: int = 0
        self.walk_frame_index: int = 0
        self.run_frame_index: int = 0
        self.animation: int = 0
        self.play_animation: dict = {
            0: self.idle_animation,
            1: self.walk_animation,
            2: self.run_animation
        }

        self.image = self.front_idle_sprites[self.idle_frame_index]
        self.rect = pygame.rect.Rect(434, 209, 32, 32)

    @property
    def direction(self) -> toolkit.Direction:

        mouse_position: tuple[int, int] = pygame.mouse.get_pos()
        dx: int = int(mouse_position[0] - self.rect.centerx)
        dy: int = int(mouse_position[1] - self.rect.centery)
        direction: toolkit.Direction = toolkit.get_direction(dx=dx, dy=dy)

        if direction.value in {315, 270, 225}:

            return Drc.EAST

        elif direction.value in {45, 90, 135}:

            return Drc.WEST

        return direction

    def idle_animation(self) -> None:

        self.animation_frame_delay = 4
        self.idle_frame_index = (self.idle_frame_index + 1) % 8
        self.image = self.idle_direction_dict.get(self.direction)[self.idle_frame_index]

    def minus_one_heart(self) -> None:

        if self.hearts and not self.invulnerable:
            self.hearts -= 1

    @property
    def now(self) -> int:

        return pygame.time.get_ticks()

    def run_animation(self) -> None:

        self.animation_frame_delay = 2
        self.run_frame_index = (self.run_frame_index + 1) % 8
        self.image = self.run_direction_dict.get(self.direction)[self.run_frame_index]

    def set_invulnerable(self, duration: int) -> None:

        if not self.invulnerable:
            self.invulnerability_time = self.now + duration
            self.invulnerable = True

    def update(self) -> None:

        mov_x, mov_y = toolkit.calculate_movement(pygame.mouse.get_pos(), self.rect, self.dead_zone, self.velocity)
        self.rect.move_ip(mov_x, mov_y)
        self.animation = 0 if (mov_x, mov_y) == (0, 0) else 1

        press_run = pygame.mouse.get_pressed()[2]

        if press_run and self.stamina > 0:
            self.animation = 2
            self.velocity = 7
            self.stamina -= 1
        else:
            self.velocity = 3
            self.stamina = self.stamina + 0.2 if self.stamina < 100 and not press_run else self.stamina

        self.invulnerable = False if self.invulnerability_time <= self.now else self.invulnerable

        if pygame.sprite.groupcollide(player_sprite, spider_sprites, False, False):

            self.minus_one_heart()
            self.set_invulnerable(duration=1200)

        self.animation_frame_delay -= 1

        if self.animation_frame_delay <= 0:

            self.play_animation[self.animation]()

    def walk_animation(self) -> None:

        self.animation_frame_delay = 4
        self.walk_frame_index = (self.walk_frame_index + 1) % 8
        self.image = self.walk_direction_dict.get(self.direction)[self.walk_frame_index]
