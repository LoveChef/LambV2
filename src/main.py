import pygame
import random
import os

from player import Player
from game_platform import Platform

pygame.init()

# Spelfönstrets bredd och höjd
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Skapar fönstret för spelet
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('LAMB')

# Sätter spelets uppdateringsfrekvens, fps = frames per second
clock = pygame.time.Clock()
FPS = 60

# Spel variabler
# * SCROLL_THRESH = 200 # jag flyttar den till player classen eftersom den används bara där.
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

# Definierar färgerna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
'''
# Definerar fontsen
font_small = font_small = pygame.font.Font(
    os.path.join("./fonts", "Poppins-SemiBold.ttf"), 20)
font_big = pygame.font.Font(
    os.path.join("./fonts", "Poppins-SemiBold.ttf"), 24)
'''

font_small = pygame.font.SysFont('Times New Roman', 20)
font_big = pygame.font.SysFont('Times New Roman', 24)

# "loadar" bilderna
char_image = pygame.image.load(
    'assets/placeholder_charachter.png').convert_alpha()
bg_image = pygame.image.load('assets/background.jpg').convert_alpha()
platform_image = pygame.image.load('assets/platform.png').convert_alpha()


# Funktion som visar texten på spelskärmen
def draw_text(text, font, text_col, x, y) -> None:
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Ritar ut bakgrunden


def draw_bg(bg_scroll) -> None:
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))


# Skapar sprite gruppen för plattformen
platform_group = pygame.sprite.Group()

# Spelar instans
char = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, GRAVITY,
              char_image, screen, SCREEN_WIDTH, platform_group)

# Skapar plattformen
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT -
                    50, 100, SCREEN_HEIGHT, platform_image)
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
        if len(platform_group) < MAX_PLATFORMS:
            # jag gjorde platformerna lite större från 40, 60 till 60, 80 (kan ändras sen om det behövs)
            p_w = random.randint(60, 80)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_w, SCREEN_HEIGHT, platform_image)
            platform_group.add(platform)

        # Uppdaterar plattformarna ju längre upp i spelet man kommer
        platform_group.update(scroll)

        # Ritar ut platform spritesen
        platform_group.draw(screen)
        char.draw()

        # Checkart om spelet är över eller inte
        if char.rect.top > SCREEN_HEIGHT:
            game_over = True
    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(
                    screen, BLACK, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(
                    screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
        draw_text('Du förlorade', font_big, WHITE, 130, 200)
        draw_text('Poäng ' + str(score), font_big, WHITE, 130, 250)
        draw_text('Klicka SPACE för att köra igen', font_big, WHITE, 40, 300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # Återställer värdena när spelet tar slut
            game_over = False
            score = 0
            scroll = 0
            fade_counter = 0
            # Flyttar tillbaka gubben till början av spelet
            char.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            # Tar bort och återställer de gamla plattformarna
            platform_group.empty()
            # Skapar en ny startplattform
            platform = Platform(SCREEN_WIDTH // 2 - 50,
                                SCREEN_HEIGHT - 50, 100, SCREEN_HEIGHT, platform_image)
            platform_group.add(platform)

    # Event handelr
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
