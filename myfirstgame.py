from cProfile import run
from tkinter import CENTER
import pygame
import random
import sys
import time
# import pygame.locals for easier access to key coordinate
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN  # If there is a keypress event      # window closure event
)


# Define constants for the screen widthh and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("jet2.png").convert()
        # set_colorkey(): any pixels that have the same color as the colorkey will be transparent
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-6)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,6)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-6,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(6,0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self .rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    def clear(self):
        self.rect.left = 0
        self.rect.top = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf = pygame.image.load("my_missile_1.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0,SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5,18)
    # Move the sprite based on speed:
    # Remove the sprite when it passed the left edge of the screen:
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud_1.png").convert()
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100),
                random.randint(0,SCREEN_HEIGHT)
            )
        )    
    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right<0:
            self.kill()
class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super(Goal,self).__init__()
        self.surf = pygame.image.load("heart1.png").convert()
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(600,SCREEN_WIDTH),
                random.randint(SCREEN_HEIGHT+20,SCREEN_HEIGHT+100)
            )
        )
        self.speed = random.randint(4,9)
    def update(self):
        self.rect.move_ip(0,-self.speed)
        if self.rect.bottom < 0:
            self.kill()
# Setup for sounds:
pygame.mixer.init()
# Initialize pygame:
pygame.init()
# Create the screen object and set the size:
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
# Set Font size:
mediumFont = pygame.font.Font("OpenSans-Regular.ttf",28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf",40)
# Load and play background music
pygame.mixer.music.load("awesomeness.wav")
pygame.mixer.music.play(loops=-1)
collision_sound = pygame.mixer.Sound("explosion.wav")
congratulation_sound = pygame.mixer.Sound("winfretless.ogg")
player = Player()
#Create groups to hold enemy sprites and all sprites
# - enemies is used for collison detection and position updates
# - clouds is used for position updates
# - all_sprites is used for rendering:

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
goals = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
# Create a custom event for adding a new enemy:
ADDENEMY = pygame.USEREVENT + 1
# And with this timer, our ADDENEMY event will occurs every 250 miliseconds
pygame.time.set_timer(ADDENEMY,350)
# And now we create a custom event for adding anew cloud:
ADDCLOUD = pygame.USEREVENT + 2
# And now we create a custom event for adding a new goal:
ADDGOAL = pygame.USEREVENT + 3
pygame.time.set_timer(ADDGOAL,3000)
pygame.time.set_timer(ADDCLOUD,1500)

surf_center = (
    (SCREEN_WIDTH - player.surf.get_width())/2,
    (SCREEN_HEIGHT - player.surf.get_height())/2
)
""" Because the frame rate is too high, it makes the missiles go very fast, to slow down, we need
    to decrease the frame rate, so we setup the clock for a decent framerate:
"""
running = True
winning = False
clock = pygame.time.Clock()
while True:

    if running == False:
        for event in pygame.event.get():
            # Was it the ESCAPE key?, If so, stop the loop
            if event.type == pygame.K_ESCAPE:
                sys.exit()
            # Did the user click the window close button? If so, stop the loop
            elif event.type == pygame.QUIT:
                sys.exit()
        screen.fill((0,0,0))
        if winning == True:
            word = largeFont.render("You Win!!",True,(0,245,255))
            wordRect = word.get_rect()
            wordRect.center = ((SCREEN_WIDTH/2,100))
            screen.blit(word,wordRect)
        
        # Draw Title:
        title = largeFont.render("Play Again?",True, (255,255,255))
        titleRect = title.get_rect()
        titleRect.center = ((SCREEN_WIDTH/2),200)
        screen.blit(title,titleRect)
        # Draw button:
        yesbutton = pygame.Rect((SCREEN_WIDTH/8),(SCREEN_HEIGHT/2),SCREEN_WIDTH/4,70)
        yes = mediumFont.render("YES",True,(0,0,0))
        yesRect = yes.get_rect()
        yesRect.center = yesbutton.center
        pygame.draw.rect(screen,(255,255,255),yesbutton)
        screen.blit(yes,yesRect)

        nobutton = pygame.Rect(5*(SCREEN_WIDTH/8),(SCREEN_HEIGHT/2),SCREEN_WIDTH/4,70)
        no = mediumFont.render("NO",True,(0,0,0))
        noRect =no.get_rect()
        noRect.center = nobutton.center
        pygame.draw.rect(screen,(255,255,255),nobutton)
        screen.blit(no,noRect)
        for event in pygame.event.get():
            pass
        # Check if button is clicked:
        click, a, b = pygame.mouse.get_pressed()
        if click:
            mouse = pygame.mouse.get_pos()
            if yesbutton.collidepoint(mouse):
                time.sleep(0.2)
                enemies.empty()
                clouds.empty()
                goals.empty()
                all_sprites.empty()
                all_sprites.add(player)
                running = True
                if winning == True:
                    winning = False
            if nobutton.collidepoint(mouse):
                time.sleep(0.2)
                sys.exit()
    else:
        # Look at every event in the queue
        for event in pygame.event.get():
            # Was it the ESCAPE key?, If so, stop the loop
            if event.type == pygame.K_ESCAPE:
                sys.exit()
            # Did the user click the window close button? If so, stop the loop
            elif event.type == pygame.QUIT:
                sys.exit()
                # If ADDENEMY occurs, we make a new enemy:
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            elif event.type == ADDGOAL:
                new_goal = Goal()
                goals.add(new_goal)
                all_sprites.add(new_goal)

        # Get  the set of keys pressed and check for user input:
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
       # Update all enemies position
        enemies.update()
       # Update all clouds position
        clouds.update()
        # Update all goals position:
        goals.update()
        # Fill the screen with white color:
        screen.fill((135,206,250))  
        # Draw all sprites on the screen
        for entity in all_sprites:
           screen.blit(entity.surf,entity.rect)
        # Check if any enemies have collided with the player:
        if pygame.sprite.spritecollideany(player,enemies):
          collision_sound.play()
          player.clear()
          running = False
        if pygame.sprite.spritecollideany(player,goals):
            congratulation_sound.play()
            player.clear()
            running = False
            winning = True
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(29)
    #update the display
    pygame.display.flip()