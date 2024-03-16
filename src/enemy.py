import pygame
import random
from constants import ANIMATION_COOLDOWN

class Enemy(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
        print(f"Initial enemy y: {y}")
        """
        Creates a new instance of the enemy class

            Args:
                SCREEN_WIDTH : The screens width
                y: The Y coordinate where the enemy will be placed on. 
                sprite_sheet: The sprite sheet that contains the enemy animations.
                scale: Scaling of the enmemy image.
        """
        
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = [] 
        self.frame_index = 0 # Index for current animation img
        self.update_time = pygame.time.get_ticks() #time for animation update   
        self.direction = random.choice([-1, 1]) #random direction left or right
        
        #flip enemy img 
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        animation_steps = 8 #total img/frames
        for animation in range(animation_steps):
            # Enemy img size + transperent
            image = sprite_sheet.get_image(animation, 500, 500, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False) #flip img
            image.set_colorkey((0, 0, 0)) #transparent
            self.animation_list.append(image)
        
        # Set the enemys current image and rectangle(hitbox)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

        # Set enemy initial position based on movement direction
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
        Updates the enemys position and the animation.

            Args:
                Scroll is the scrollspeed of the game
                screen_width Is the width of the game
        """
        self.rect.x += self.direction * 2

        self.image = self.animation_list[self.frame_index]
        # Check if enough time has passed to update the animation
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            #update timer
            self.update_time = pygame.time.get_ticks()
            #Shows next frame
            self.frame_index += 1
            #resets fram index when enemy reches the end
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                
        #updates position
        self.rect.x += self.direction * 2
        self.rect.y += scroll
    
        # Check if enemy goes off the screen and kills it
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
