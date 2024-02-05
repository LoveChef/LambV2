import pygame

WHITE = (255, 255, 255)


class Player:
    def __init__(self, x, y, gravity, char_image, screen, screen_width, platform_group) -> None:
        """Initialze the player

        Args:
            x (int): The x coordinate of the player
            y (int): The y coordinate of the player
            gravity (float): The gravity effecting the players jumping distance
            screen_width (int): The width of the screen
            platform_group (platform.sprite.group): The group including the platform sprites
        """
        self.image = pygame.transform.scale(
            char_image, (45, 45))  # Skapar gubben och anpassar storleken
        # Gubbens höjd och bredd
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.center = (x, y)  # Centrerar gubben på sin kordinat

        # hastighet & riktning
        self.vel_y = 0
        self.flip = False

        # Nya variabler jag behövde skapa för att flytta Player till en ny fil
        self.scroll_thresh = 200
        self.gravity = gravity
        self.screen_width = screen_width
        self.platform_group = platform_group
        self.screen = screen

    def move(self) -> None:
        """_summary_

        Returns:
            Int: The verticial scorlling amount
        """
        # Återställer variabler
        scroll = 0
        dx = 0
        dy = 0

        # Hanterar knappttryck
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        # Spelets gravitation
        self.vel_y += self.gravity
        dy += self.vel_y

        # Gör så att spelar inte kan hamna utanför spelets fönster
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > self.screen_width:
            dx = self.screen_width - self.rect.right

        # Kollar ifall spelar nuddar plattformarna
        for platform in self.platform_group:
            # Kollar i y
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Kollar om den är ovanför
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        # Ser ifall gubben nått toppen av skärmen
        if self.rect.top <= self.scroll_thresh:
            if self.vel_y < 0:
                scroll = -dy

        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self) -> None:
        self.screen.blit(pygame.transform.flip(
            self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
        pygame.draw.rect(self.screen, WHITE, self.rect, 2)
