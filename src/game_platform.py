import pygame


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width, screen_height, platform_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # nya variabel
        self.screen_height = screen_height

    def update(self, scroll) -> None:

        # Uppdaterar plattformens position vertikalt
        self.rect.y += scroll

        # check if platform has gone off the screen
        if self.rect.top > self.screen_height:
            self.kill()
