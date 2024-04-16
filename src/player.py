import pygame

from constants import SCREEN_WIDTH, WHITE, GRAVITY

class Player:
    def __init__(self, x, y, char_image, screen, platform_group) -> None:
        """Initialze the player

        Args:
            x : The x coordinate of the player
            y : The y coordinate of the player
            platform_group : The group including the platform sprites
        """
        self.image = pygame.transform.scale(
            char_image, (75, 75))  # Creates the charachter and adapts the size
        # Charchters height and width
        self.width = 35
        self.height = 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.center = (x, y)  # Centers the charchters on the coordinates

        # Velocity and direction
        self.vel_y = 0
        self.flip = True

        # New variables 
        self.scroll_thresh = 200
        self.platform_group = platform_group
        self.screen = screen

    def move(self) -> None:
        """Handles player movement 

        Returns:
            Int: The verticial scorlling amount
        """
        # Resets the variables
        scroll = 0
        dx = 0
        dy = 0

        # Handles key pressing
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = False
        if key[pygame.K_d]:
            dx = 10
            self.flip = True
        if key[pygame.K_LEFT]:
            dx = -10
            self.flip = False
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = True

        # The games gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Makes so the player cant go outside the games screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # Checks if the player is on a platform and if the player is above
        for platform in self.platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        # Checks if the player has reached the top of the screen
        if self.rect.top <= self.scroll_thresh:
            if self.vel_y < 0:
                scroll = -dy

        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self) -> None:
        """
        Draws the game
        
        """
        self.screen.blit(pygame.transform.flip(
            self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
