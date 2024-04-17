import pygame
import random
import os
from player import Player
from game_platform import Platform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, PANEL, SCORE_FILE_PATH, FONTS_FILE_PATH, FONT_NAME, MAX_PLATFORMS
from sprite import Spritesheet
from enemy import Enemy

pygame.init()
# Icon
icon = pygame.image.load("../assets/icon.png")
pygame.display.set_icon(icon)

# Creates the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LAMB")

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
    with open(SCORE_FILE_PATH, "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Loads the images
char_image = pygame.image.load("../assets/charachter.png").convert_alpha()
bg_image = pygame.image.load("../assets/background.jpg").convert_alpha()
platform_image = pygame.image.load("../assets/platform.png").convert_alpha()
bird_img = pygame.image.load("../assets/enemy_spritesheet.png").convert_alpha()
bird_sheet = Spritesheet(bird_img)

# Music
pygame.mixer.music.load("../assets/music.mp3")

# Creates the sprite for the platforms
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

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
    draw_text("Poäng: " + str(score), font_small, WHITE, 150, 0)

# Draws the background
def draw_bg(bg_scroll) -> None:
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))


def show_start_screen():
    start_screen_image = pygame.image.load("../assets/startscreen.png").convert_alpha()
    screen.blit(start_screen_image, (0, 0))
    pygame.display.update()

start_screen = True

music_playing = False

# Main loop
run = True
while run:
    clock.tick(FPS)
    if start_screen:
        show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_screen = False
                
        

    else:
        if not music_playing: # Starts the music and loops it
            pygame.mixer.music.play(-1)
            music_playing = True


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
                p_type = random.randint(1, 5)
                # Checks if platform is movable, the higher up the more platforms can move
                # 100% # Below the percentages repersent how high the percentage that the platforsms will move
                if p_type in [1, 2, 3, 4, 5] and score > 200:
                    p_moving = True
                # 80%
                elif  p_type in [1, 2, 3, 4] and score > 100:
                    p_moving = True
                # 40%
                elif p_type in [1, 2] and score > 75:
                    p_moving = True
                # 20%
                elif p_type == 1 and score > 50:
                    p_moving = True
                else:
                    p_moving = False

                platform = Platform(p_x, p_y, p_w, platform_image, p_moving)
                platform_group.add(platform)

            # Updates the platforms the further you go up
            platform_group.update(scroll)
        
            if score % 10 == 0 and len(enemy_group) == 0 and score != 0:  # Check for score and no existing enemies
                player_height = char.rect.height
                enemy = Enemy(SCREEN_WIDTH, 5, bird_sheet, 0.1)  # Create enemy
                enemy.rect.y = char.rect.top - enemy.rect.height  # Position above character
                enemy_group.add(enemy)  # Add enemy to group
    
            enemy_group.update(scroll, SCREEN_WIDTH)

            # Sound that plays when  the player earns a point
            score_sound = pygame.mixer.Sound("../assets/coin.mp3")
            
            #Sound that plays whenever the player losees
            lose_sound = pygame.mixer.Sound("../assets/lose.wav")

            # Update score
            
            for platform in platform_group:
                if pygame.sprite.collide_rect(char, platform):
                    if not platform.point_given:
                        score += 1
                        platform.point_given = True
                        score_sound.play()

            # Draws the sprites
            platform_group.draw(screen)
            enemy_group.draw(screen)
            char.draw()
            
            draw_panel()

            # Checks if the game is over
            if char.rect.top > SCREEN_HEIGHT:
                game_over = True
                lose_sound.play()
            if pygame.sprite.spritecollide(char, enemy_group, False):
                if pygame.sprite.spritecollide(char, enemy_group, False, pygame.sprite.collide_mask): 
                    game_over = True
                    lose_sound.play()
            

        else:
            pygame.mixer.music.stop()
            draw_text("Du förlorade", font_big, WHITE, 130, 200)
            draw_text("Poäng " + str(score), font_big, WHITE, 130, 250)
            draw_text("Klicka SPACE för att köra igen", font_big, WHITE, 25, 300)
            draw_text("Klicka ESC för att stänga", font_big, WHITE, 45, 400)
            if score > high_score:
                high_score = score
                with open(SCORE_FILE_PATH, "w") as file:
                    file.write(str(high_score)) 
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # Resets the platforms when the game is over
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                char.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                enemy_group.empty()
                platform_group.empty()
                platform = Platform(SCREEN_WIDTH // 2 - 50,
                                    SCREEN_HEIGHT - 50, 100, platform_image, False)
                platform_group.add(platform)
                pygame.mixer.music.play(-1)

                if not music_playing:
                    pygame.mixer.music.play(-1)
                    music_playing = True

            if key[pygame.K_ESCAPE]:
                run = False

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

                # update high_score
                if score > high_score:
                    high_score = score
                    with open(SCORE_FILE_PATH, "w") as file:
                        file.write(str(high_score)) 

        pygame.display.update()

pygame.quit()
