"""
This module contains everything related to spiders.
"""

import pygame
from random import randint, uniform, choice
from pathlib import Path

from modules import constants
from modules import toolkit


spider_sprites = pygame.sprite.Group()
spider_blood_effects = pygame.sprite.Group()


class Spider(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.game_surface: pygame.Surface = pygame.display.get_surface()

        self.velocity: int = 0
        self.spawn_position: tuple[int, int]
        self.direction: toolkit.Direction = toolkit.Direction.NONE
        self.attacking: bool = False
        self.idle_frame_index: int = 0
        self.attacking_frame_index: int = 0
        self.animation_frame_delay: int = 0

        ##############################
        # Assets.
        ##############################

        self.assets: dict = toolkit.load_images(folder=Path(constants.GRAPHICS_DIR / "spiders"), alpha=True)

        self.adult_idle_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("idle_green_spiders"),
            sprites_size=64,
            sprites_number=7
        ).sprite_surfaces()

        self.baby_idle_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("idle_red_spiders"),
            sprites_size=64,
            sprites_number=7
        ).sprite_surfaces(0.7)

        self.adult_attacking_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("attack_green_spiders"),
            sprites_size=64,
            sprites_number=3
        ).sprite_surfaces()

        self.baby_attacking_sprites: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=self.assets.get("attack_red_spiders"),
            sprites_size=64,
            sprites_number=3
        ).sprite_surfaces(0.7)

        ##############################

        self.image: pygame.Surface
        self.rect: pygame.Rect

    def attack_animation(self) -> None:

        ...

    def draw_shadow(self) -> None:

        spider_shadow: pygame.Surface = toolkit.get_shadow_surface(self.image)
        self.game_surface.blit(spider_shadow, (self.rect.x - 4, self.rect.y + 4))

    def get_direction(self, player_position: tuple[int, int]) -> toolkit.Direction:
        """Determines the direction in which a spider moves.

        Args:
            player_position (tuple[int, int]): The position of the player as a tuple of (x, y) coordinates.

        Returns:
            toolkit.Direction: The direction as an instance of toolkit.Direction enum.
        """

        dx: int = int(player_position[0] - self.rect.centerx)
        dy: int = int(player_position[1] - self.rect.centery)
        return toolkit.get_direction(dx=dx, dy=dy)

    def idle_animation(self) -> None:

        ...

    def kill(self):

        spider_blood_effects.add(SpiderBloodSplat(position=self.rect.center))   # type: ignore
        spider_blood_effects.add(SpiderBloodSplash(position=self.rect.center))  # type: ignore

        super().kill()

    def update(self, player_position: tuple[int, int]) -> None:

        mov_x, mov_y = toolkit.calculate_movement(player_position, self.rect, 15, self.velocity)
        self.rect.move_ip(mov_x, mov_y)

        self.animation_frame_delay -= 1
        self.attacking = True if (mov_x, mov_y) == (0, 0) else False
        self.direction = self.get_direction(player_position=player_position)

        if self.animation_frame_delay <= 0 and not self.attacking:

            self.idle_animation()

        elif self.animation_frame_delay <= 0 and self.attacking:

            self.attack_animation()

        # It's important to recenter the rectangle because rotation alters the image's dimensions.
        self.rect = self.image.get_rect(center=self.rect.center)


class AdultSpider(Spider):

    def __init__(self):
        super().__init__()

        self.velocity = 2
        self.spawn_position = self.randomize_spawn_location()

        self.image = self.adult_idle_sprites[self.idle_frame_index]
        self.rect = pygame.rect.Rect(*self.spawn_position, 32, 32)

    def attack_animation(self) -> None:

        self.animation_frame_delay = 12
        self.attacking_frame_index = (self.attacking_frame_index + 1) % len(self.adult_attacking_sprites)

        image = pygame.transform.rotate(self.adult_attacking_sprites[self.attacking_frame_index], self.direction.value)
        self.image = image

    def idle_animation(self) -> None:

        self.animation_frame_delay = 6
        self.idle_frame_index = (self.idle_frame_index + 1) % len(self.adult_idle_sprites)

        image = pygame.transform.rotate(self.adult_idle_sprites[self.idle_frame_index], self.direction.value)
        self.image = image

    def kill(self) -> None:

        if not randint(a=0, b=2):  # 1 in 3 chance to lay eggs.
            self.spawn_babies()

        super().kill()

    def randomize_spawn_location(self) -> tuple[int, int]:
        """Generate a random spawn location for a spider.

        Returns:
            tuple[int, int]: A tuple containing the randomly generated x and y coordinates.
        """

        random_x_spawn: int = randint(-100, 1000)
        random_y_spawn: int = randint(-100, 550)

        if not (-32 <= random_x_spawn <= 982) or not (-32 <= random_y_spawn <= 582):
            return random_x_spawn, random_y_spawn
        return self.randomize_spawn_location()

    def spawn_babies(self) -> None:

        for i in range(randint(a=1, b=5)):
            spider_sprites.add(BabySpider((self.rect.centerx - 20 * i, self.rect.centery - 20 * i)))  # type: ignore


class BabySpider(Spider):

    def __init__(self, spawn_position: tuple[int, int]):
        super().__init__()

        self.velocity = 3
        self.spawn_position = spawn_position

        self.image = self.baby_idle_sprites[self.idle_frame_index]
        self.rect = pygame.rect.Rect(*self.spawn_position, 24, 24)

    def attack_animation(self) -> None:

        self.animation_frame_delay = 6
        self.attacking_frame_index = (self.attacking_frame_index + 1) % len(self.baby_attacking_sprites)

        image = pygame.transform.rotate(self.baby_attacking_sprites[self.attacking_frame_index], self.direction.value)
        self.image = image

    def idle_animation(self) -> None:

        self.animation_frame_delay = 3
        self.idle_frame_index = (self.idle_frame_index + 1) % len(self.baby_idle_sprites)

        image = pygame.transform.rotate(self.baby_idle_sprites[self.idle_frame_index], self.direction.value)
        self.image = image


class SpiderBloodSplash(pygame.sprite.Sprite):
    """
    This class manages the animation of a blood splash when a spider is destroyed.
    The animation consists of a series of images representing a blood splash,
    which are displayed successively to create a visual effect of damage or destruction.
    """

    def __init__(self, position: tuple[int, int]):
        super().__init__()

        adjusted_position: tuple[int, int] = position[0] - 90, position[1] - 90

        assets: dict = toolkit.load_images(
            folder=Path(constants.GRAPHICS_DIR / "spiders", "blood"),
            alpha=True
        )

        self.animation_frames: list[pygame.Surface] = list(assets.values())
        self.animation_frame_index: int = 0
        self.animation_frame_delay: int = 0

        self.image = self.animation_frames[self.animation_frame_index]
        self.rect = pygame.Rect(*adjusted_position, 32, 32)

    def play_animation(self) -> None:

        self.animation_frame_delay = 1
        self.animation_frame_index = (self.animation_frame_index + 1) % len(self.animation_frames)

        frame = self.animation_frames[self.animation_frame_index]
        scaled_frame = pygame.transform.scale2x(frame)

        self.image = scaled_frame

        if self.animation_frame_index >= 28:
            self.kill()

    def update(self) -> None:

        self.animation_frame_delay -= 1

        if self.animation_frame_delay <= 0:

            self.play_animation()


class SpiderBloodSplat(pygame.sprite.Sprite):
    """
    A class representing blood splats left by spiders.
    """

    def __init__(self, position: tuple[int, int]):
        super().__init__()

        adjusted_position: tuple[int, int] = position[0] - 30, position[1] - 30

        ##############################
        # Assets.
        ##############################

        blood_splats_file: Path = Path(constants.GRAPHICS_DIR / "spiders", "blood_splats.png")
        blood_splats: pygame.Surface = pygame.image.load(blood_splats_file).convert_alpha()

        self.blood_splats_list: list[pygame.Surface] = toolkit.SpritesLoader(
            sprites_image=blood_splats,
            sprites_size=256,
            sprites_number=5
        ).sprite_surfaces()

        ##############################

        self.opacity: int = 100
        self.animation_frame_delay: int = 100

        self.image: pygame.Surface = self.randomize_splat()
        self.rect: pygame.Rect = pygame.Rect(*adjusted_position, 32, 32)

    def randomize_splat(self) -> pygame.Surface:
        """Randomly selects a blood splat image, rotates and scales it, and returns the modified surface.

        Returns:
            pygame.Surface: The modified blood splat image.
        """

        scale_factor: float = uniform(a=0.20, b=0.25)
        selected_splat: pygame.Surface = choice(self.blood_splats_list)
        rotated_splat = pygame.transform.rotate(selected_splat, randint(a=1, b=360))
        scaled_and_rotated_splat = pygame.transform.scale(
            surface=rotated_splat,
            size=(rotated_splat.get_width() * scale_factor, rotated_splat.get_height() * scale_factor)
        )

        return scaled_and_rotated_splat

    def update(self) -> None:

        self.animation_frame_delay -= 1

        if self.animation_frame_delay <= 0:

            self.animation_frame_delay = 5
            self.opacity -= 1
            self.image.set_alpha(self.opacity)

        if self.opacity <= 0:
            self.kill()
