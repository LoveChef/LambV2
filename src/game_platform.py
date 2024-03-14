import random
import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Platform(pygame.sprite.Sprite):
    """Class for platforms 

    Args:
        x (int): The x coordinate for the platform
        y (int): The y coordinate for the platform
        width (int): The width of the platform
    """
    def __init__(self, x, y, width, platform_image, moving, point_given=False) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.point_given = False

        # Moving platform variables
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = (random.choice([-1, 1]))
        self.speed = random.randint(1, 2)

    def update(self, scroll) -> None:
        """Update the platforms position

        Args:
            scroll (int): The verticial scrolling value
        """
        # Platform movement
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0

        # Update the platforms vertical position
        self.rect.y += scroll

        # checks if the platform has gone off the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
