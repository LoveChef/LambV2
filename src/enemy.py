import pygame
import random
from constants import ANIMATION_COOLDOWN

class Enemy(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
        print(f"Initial enemy y: {y}")
        """
        Creates a new instance of the enemy class

            Args:
                SCREEN_WIDTH (int) : The screens width
                y (int) : The Y coordinate where the enemy will be placed on. 
                sprite_sheet (objekt) : The sprite sheet that contains the enemy animations.
                scale (float) : Scaling of the enmemy image.
        """
        
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()       
        self.direction = random.choice([-1, 1])
        
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        animation_steps = 8
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, 500, 500, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)
        
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

        if self.direction == 1:
            self.rect.x = 0
            self.start_pos = 0
            self.end_pos = SCREEN_WIDTH
        else:
            self.rect.x = SCREEN_WIDTH
            self.start_pos = SCREEN_WIDTH
            self.end_pos = 0
            self.rect.y = y

    def update(self, scroll, SCREEN_WIDTH):
        """
        Uppdaterar fiendens position och animationen.z

            Args:
                scroll är scrollhastigheten i spelet.
                screen_width är bredden på spelområdet.
        """
        self.rect.x += self.direction * 2

        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

        self.rect.x += self.direction * 2
        self.rect.y += scroll
    
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
