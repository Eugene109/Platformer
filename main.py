from tkinter import Widget
import pygame
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
    def move(self):
        pass
 
    def update(self):
        pass
    
    def attack(self):
        pass
    
    def jump(self):
        pass
     
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


background = Background()
ground = Ground()
player = Player()
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
            pass

    # Render Functions ------
    background.render()
    ground.render()
    displaysurface.blit(player.image, player.rect)
 
    pygame.display.update() 
    FPS_CLOCK.tick(FPS)