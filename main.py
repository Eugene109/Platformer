from multiprocessing.dummy import current_process
import pkgutil
from platform import platform
from tkinter import Widget
from turtle import width
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
ACC = 0.6
FRIC = -0.10
FPS = 45
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

camPos = vec(0,0)

class Background(pygame.sprite.Sprite):
    def __init__(self, fName):
        super().__init__()
        self.bgimage = pygame.image.load(fName)
        self.bgimage = pygame.transform.scale(self.bgimage, (self.bgimage.get_width()/2, self.bgimage.get_height()/2))
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
 
 
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./res/ground.png")
        self.image = pygame.transform.scale(self.image, (WIDTH*4, HEIGHT/2))
        self.rect = self.image.get_rect(center = (WIDTH*2, HEIGHT*3/4))
 
    def render(self):
        displaysurface.blit(self.image, (self.rect.x - camPos.x, self.rect.y - camPos.y))
        # displaysurface.blit(self.image, (self.rect.x, self.rect.y))


class Platform(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("./res/platform.png")
        self.image = pygame.transform.scale(self.image, (1650/16, 560/16))
        self.rect = self.image.get_rect(center = position)
 
    def render(self):
        displaysurface.blit(self.image, (self.rect.x - camPos.x, self.rect.y - camPos.y))
        # displaysurface.blit(self.image, (self.rect.x, self.rect.y))




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./res/sprite/0000.png")
        self.run_anim = [
            pygame.image.load("./res/sprite/0000.png"), pygame.image.load("./res/sprite/0001.png"), pygame.image.load("./res/sprite/0002.png"),
            pygame.image.load("./res/sprite/0003.png"), pygame.image.load("./res/sprite/0004.png"), pygame.image.load("./res/sprite/0005.png"),
            pygame.image.load("./res/sprite/0006.png"), pygame.image.load("./res/sprite/0007.png"), pygame.image.load("./res/sprite/0008.png"),
            pygame.image.load("./res/sprite/0009.png"), pygame.image.load("./res/sprite/0010.png"), pygame.image.load("./res/sprite/0011.png"),
            pygame.image.load("./res/sprite/0012.png"), pygame.image.load("./res/sprite/0013.png"), pygame.image.load("./res/sprite/0014.png"),
            pygame.image.load("./res/sprite/0015.png"), pygame.image.load("./res/sprite/0016.png"), pygame.image.load("./res/sprite/0017.png"),
            pygame.image.load("./res/sprite/0018.png"), pygame.image.load("./res/sprite/0019.png"), pygame.image.load("./res/sprite/0020.png"),
            pygame.image.load("./res/sprite/0021.png"), pygame.image.load("./res/sprite/0022.png"), pygame.image.load("./res/sprite/0023.png"),
            pygame.image.load("./res/sprite/0024.png"), pygame.image.load("./res/sprite/0025.png"), pygame.image.load("./res/sprite/0026.png"),
            pygame.image.load("./res/sprite/0027.png"), pygame.image.load("./res/sprite/0028.png"), pygame.image.load("./res/sprite/0029.png"),
            pygame.image.load("./res/sprite/0030.png"), pygame.image.load("./res/sprite/0031.png"), pygame.image.load("./res/sprite/0032.png")
        ]
        self.rect = pygame.Rect(WIDTH/2, HEIGHT/2, self.image.get_width()/2, self.image.get_height())
 
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

        self.rect.y -= 1
        hits = pygame.sprite.spritecollide(player, collision_group, False)
        if hits:
            closest = hits[0]
            width = closest.rect.right - closest.rect.left
            r = closest.rect.left - self.rect.right # negative == collision
            l = self.rect.left - closest.rect.right # negative == collision
            # print(r)
            # print(l)
            if abs(r) < width and r < 0:
                if self.acc.x > 0:
                    self.acc.x = 0
                if self.vel.x > 0:
                    self.vel.x = 0
            if abs(l) < width and l < 0:
                if self.acc.x < 0:
                    self.acc.x = 0
                if self.vel.x < 0:
                    self.vel.x = 0
    
        self.rect.y += 1


        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values

        # Update rect with new pos 
        self.rect.midbottom = self.pos

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, collision_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def update(self):
        # Return to base frame if at end of movement sequence 
        if self.move_frame > 32:
            self.move_frame = 1
            return
        # Move the character to the next frame if conditions are met 
        if self.running == True:  
            if self.vel.x > 0:
                self.image = pygame.transform.flip(self.run_anim[int(self.move_frame)], True, False)
                self.direction = "RIGHT"
            else:
                self.image = self.run_anim[int(self.move_frame)]
                self.direction = "LEFT"
            if self.jumping == False:
                self.move_frame += 1
            else:
                self.move_frame += 0.2
            # Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.5 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = pygame.transform.flip(self.run_anim[int(self.move_frame)], True, False)
            elif self.direction == "LEFT":
                self.image = self.run_anim[int(self.move_frame)]

    def attack(self):
        pass
    
    def jump(self):
        self.rect.x += 1
    
        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, collision_group, False)
        
        self.rect.x -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


background = Background("./res/background.png")
midground = Background("./res/midground.png")
midground.bgY = 100

ground = Ground()
player = Player()
platforms = [Platform((560, 170)), Platform((650, 40))]

collision_group = pygame.sprite.Group()
collision_group.add(ground)
for current_platform in platforms:
    collision_group.add(current_platform)

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
    player.update()
    player.move()

    camPos = player.pos - vec(WIDTH/2, HEIGHT/2)

    r = platforms[0].rect.left - player.rect.right # negative == collision
    l = player.rect.left - platforms[0].rect.right 
    print(r)
    print(l)


    # Render Functions ------
    background.render()
    midground.render()
    # midground.bgX -= camPos.x/3
    # midground.bgY -= camPos.y/3
    ground.render()
    for current_platform in platforms:
        current_platform.render()
    displaysurface.blit(player.image, (WIDTH/2 - player.image.get_width()/2, HEIGHT/2 - player.image.get_height()))
 
    pygame.display.update() 
    FPS_CLOCK.tick(FPS)