import pygame


class Platform(pygame.sprite.Sprite):
    """Class for platforms 

    Args:
        x (int): The x coordinate for the platform
        y (int): The y coordinate for the platform
        width (int): The width of the platform
        screen_height (int): Screen height  
    """
    def __init__(self, x, y, width, screen_height, platform_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.screen_height = screen_height

    def update(self, scroll) -> None:
        """Update the platforms position

        Args:
            scroll (int): The verticial scrolling value
        """
        # Update the platforms vertical position
        self.rect.y += scroll

        # checks if the platform has gone off the screen
        if self.rect.top > self.screen_height:
            self.kill()
