import pygame
import random
import os
from player import Player
from game_platform import Platform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, PANEL, SCORE_FILE_PATH, FONTS_FILE_PATH, FONT_NAME, MAX_PLATFORMS

pygame.init()
# Icon
icon = pygame.image.load('../assets/icon.png')
pygame.display.set_icon(icon)

# Creates the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('LAMB')

# Updating frequency
clock = pygame.time.Clock()
FPS = 60

# Game variables
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

# Definerar fontsen
font_small = font_small = pygame.font.Font(
    os.path.join(FONTS_FILE_PATH, FONT_NAME), 20)
font_big = pygame.font.Font(
    os.path.join(FONTS_FILE_PATH, FONT_NAME), 24)

# load high_score
if os.path.exists(SCORE_FILE_PATH):
    with open(SCORE_FILE_PATH, 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# Loads the images
char_image = pygame.image.load(
    '../assets/charachter.png').convert_alpha()
bg_image = pygame.image.load('../assets/background.jpg').convert_alpha()
platform_image = pygame.image.load('../assets/platform.png').convert_alpha()

# Creates the sprite for the platforms
platform_group = pygame.sprite.Group()

# Player instance
char = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, char_image, screen, platform_group)

# Creates platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT -
                    50, 100, platform_image, False)
platform_group.add(platform)

# Function that shows the text
def draw_text(text, font, text_col, x, y) -> None:
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for info panel
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)

# Draws the background
def draw_bg(bg_scroll) -> None:
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))

# Main loop
run = True
while run:

    clock.tick(FPS)

    if game_over == False:
        scroll = char.move()

        # Draws the background in the window
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        # Generates the platform the charachter jumps on
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(60, 80)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            # Determines if platformi is moving
            p_type = random.randint(1, 5)
            print(p_type)
            # Checks if platform is movable, the higher up the more platforms can move
            # 100% that it moves
            if p_type in [1, 2, 3, 4, 5] and score > 20000:
                p_moving = True
            # 80%
            elif  p_type in [1, 2, 3, 4] and score > 10000:
                p_moving = True
            # 40%
            elif p_type in [1, 2] and score > 3000:
                p_moving = True
            # 20%
            elif p_type == 1 and score > 500:
                p_moving = True
            else:
                p_moving = False

            platform = Platform(p_x, p_y, p_w, platform_image, p_moving)
            platform_group.add(platform)

        # Updates the platforms the further you go up
        platform_group.update(scroll)

        # Update score
        if scroll > 0:
            score += scroll
        print(score)
        # Draws the sprites
        platform_group.draw(screen)
        char.draw()

        draw_panel()

        # Checks if the game is over
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
        if score > high_score:
            high_score = score
            with open(SCORE_FILE_PATH, 'w') as file:
                file.write(str(high_score))
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # Resets the platforms when the game is over
            game_over = False
            score = 0
            scroll = 0
            fade_counter = 0
            char.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            platform_group.empty()
            platform = Platform(SCREEN_WIDTH // 2 - 50,
                                SCREEN_HEIGHT - 50, 100, platform_image, False)
            platform_group.add(platform)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

            # update high_score
            if score > high_score:
                high_score = score
                with open(SCORE_FILE_PATH, 'w') as file:
                    file.write(str(high_score))

    pygame.display.update()

pygame.quit()
