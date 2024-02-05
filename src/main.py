import pygame
import random
import os

from player import Player
from game_platform import Platform

pygame.init()

# Game width and height
screen_width = 400
screen_height = 600

# Creates the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('LAMB')

# Updating frequency
clock = pygame.time.Clock()
FPS = 60

# Game variables
gravity = 1
max_platforms = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

# Defines the colors
white = (255, 255, 255)
black = (0, 0, 0)
'''
# Definerar fontsen
font_small = font_small = pygame.font.Font(
    os.path.join("./fonts", "Poppins-SemiBold.ttf"), 20)
font_big = pygame.font.Font(
    os.path.join("./fonts", "Poppins-SemiBold.ttf"), 24)
'''

font_small = pygame.font.SysFont('Times New Roman', 20)
font_big = pygame.font.SysFont('Times New Roman', 24)

# Loads the images
char_image = pygame.image.load(
    'assets/placeholder_charachter.png').convert_alpha()
bg_image = pygame.image.load('assets/background.jpg').convert_alpha()
platform_image = pygame.image.load('assets/platform.png').convert_alpha()


# Function that shows the text
def draw_text(text, font, text_col, x, y) -> None:
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Draws the background


def draw_bg(bg_scroll) -> None:
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))


# Skapar sprite gruppen för plattformen
platform_group = pygame.sprite.Group()

# Spelar instans
char = Player(screen_width // 2, screen_height - 150, gravity,
              char_image, screen, screen_width, platform_group)

# Skapar plattformen
platform = Platform(screen_width // 2 - 50, screen_height -
                    50, 100, screen_height, platform_image)
platform_group.add(platform)

# Spelets main loop
run = True
while run:

    clock.tick(FPS)

    if game_over == False:
        scroll = char.move()

        # "Ritar ut" bakgrunden i fönstret
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        # Generera plattformen som gubben hoppar på
        if len(platform_group) < max_platforms:
            # jag gjorde platformerna lite större från 40, 60 till 60, 80 (kan ändras sen om det behövs)
            p_w = random.randint(60, 80)
            p_x = random.randint(0, screen_width - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_w, screen_height, platform_image)
            platform_group.add(platform)

        # Uppdaterar plattformarna ju längre upp i spelet man kommer
        platform_group.update(scroll)

        # Ritar ut platform spritesen
        platform_group.draw(screen)
        char.draw()

        # Checkart om spelet är över eller inte
        if char.rect.top > screen_height:
            game_over = True
    else:
        if fade_counter < screen_width:
            fade_counter += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(
                    screen, black, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(
                    screen, black, (screen_width - fade_counter, (y + 1) * 100, screen_width, 100))
        draw_text('Du förlorade', font_big, white, 130, 200)
        draw_text('Poäng ' + str(score), font_big, white, 130, 250)
        draw_text('Klicka SPACE för att köra igen', font_big, white, 40, 300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # Återställer värdena när spelet tar slut
            game_over = False
            score = 0
            scroll = 0
            fade_counter = 0
            # Flyttar tillbaka gubben till början av spelet
            char.rect.center = (screen_width // 2, screen_height - 150)
            # Tar bort och återställer de gamla plattformarna
            platform_group.empty()
            # Skapar en ny startplattform
            platform = Platform(screen_width // 2 - 50,
                                screen_height - 50, 100, screen_height, platform_image)
            platform_group.add(platform)

    # Event handelr
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
