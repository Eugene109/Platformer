from tkinter import Widget
import pygame
from pygame.locals import *
import sys
import math
import random

pygame.init()  # Begin pygame
 
# Declaring variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 540
WIDTH = 960
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Background(pygame.sprite.Sprite):
    def __init__(self):
            super().__init__()
            self.bgimage = pygame.image.load("./res/background.png")
            self.bgimage = pygame.transform.scale(self.bgimage, (WIDTH, HEIGHT))
            self.bgY = 0
            self.bgX = 0

    def render(self):
            displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
 
 
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./res/ground.png")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT/2))
        self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT*3/4))
 
    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))  

 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./res/0001.png")
        self.image = pygame.transform.scale(self.image, (WIDTH/6, WIDTH/6))
        self.rect = self.image.get_rect()
 
        # Position and direction
        self.vx = 0
        self.pos = vec((WIDTH/2, HEIGHT/2))
        self.vel = vec(0,0) 
        self.acc = vec(0,0)
        self.direction = "RIGHT"

        # Movement 
        self.jumping = False
        self.running = False
        self.move_frame = 0

    def move(self):
        # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
        self.acc = vec(0,0.5)

        # Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False
        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()
    
        # Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
                self.acc.x = -ACC
                self.direction = "LEFT"
        if pressed_keys[K_RIGHT]:
                self.acc.x = ACC 
                self.direction = "RIGHT"
    
        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values
    
        # This causes character warping from one point of the screen to the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos  # Update rect with new pos 
    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player ,ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def update(self):
        pass
    
    def attack(self):
        pass
    
    def jump(self):
        self.rect.x += 1
    
        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        
        self.rect.x -= 1
    
        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


background = Background()
ground = Ground()
player = Player()

ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

while True:
    for event in pygame.event.get():
        # Will run when the close window button is clicked    
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
        # For events that occur upon clicking the mouse (left click) 
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
 
        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE:
                  player.jump()

    # update player

    player.gravity_check()
    player.move()

    # Render Functions ------
    background.render()
    ground.render()
    displaysurface.blit(player.image, player.rect)
 
    pygame.display.update() 
    FPS_CLOCK.tick(FPS)