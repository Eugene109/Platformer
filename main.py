from pickle import TRUE
from platform import platform
from tkinter import Widget
from turtle import width
from xml.etree.ElementTree import tostring
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
        self.image = pygame.transform.scale(self.image, (WIDTH*4, HEIGHT/2+2))
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
        self.explosion_anim = [
            pygame.image.load("./res/explosion/tile001.png"), pygame.image.load("./res/explosion/tile002.png"), pygame.image.load("./res/explosion/tile003.png"),
            pygame.image.load("./res/explosion/tile004.png"), pygame.image.load("./res/explosion/tile005.png"), pygame.image.load("./res/explosion/tile006.png"),
            pygame.image.load("./res/explosion/tile007.png"), pygame.image.load("./res/explosion/tile008.png"), pygame.image.load("./res/explosion/tile009.png"),
            pygame.image.load("./res/explosion/tile009.png"), pygame.image.load("./res/explosion/tile011.png"), pygame.image.load("./res/explosion/tile012.png"),
            pygame.image.load("./res/explosion/tile013.png"), pygame.image.load("./res/explosion/tile014.png"), pygame.image.load("./res/explosion/tile015.png")
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
        self.dead = False
        self.num_batteries = 0

    def move(self):
        # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
        self.acc = vec(0,0.4)

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

        self.rect.y -= 2
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
    
        self.rect.y += 2


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
    
    def obst_check(self):
        hits = pygame.sprite.spritecollide(player, obstacle_group, False)
        if hits:
            closest = hits[0]
            width = closest.rect.right - closest.rect.left
            height = closest.rect.bottom - closest.rect.top
            r = closest.rect.left - self.rect.right # negative == collision
            l = self.rect.left - closest.rect.right # negative == collision
            b = closest.rect.top - self.rect.bottom # negative == collision
            t = self.rect.top - closest.rect.bottom # negative == collision

            if abs(r) < width and r < 0:
                self.dead = True
                self.move_frame = 0
            if abs(l) < width and l < 0:
                self.dead = True
                self.move_frame = 0
            if abs(b) < height and b < 0:
                self.dead = True
                self.move_frame = 0
            if abs(t) < height and t < 0:
                self.dead = True
                self.move_frame = 0

    def battery_check(self):
        hits = pygame.sprite.spritecollide(player, battery_group, False)
        if hits:
            closest = hits[0]
            width = closest.rect.right - closest.rect.left
            height = closest.rect.bottom - closest.rect.top
            r = closest.rect.left - self.rect.right # negative == collision
            l = self.rect.left - closest.rect.right # negative == collision
            b = closest.rect.top - self.rect.bottom # negative == collision
            t = self.rect.top - closest.rect.bottom # negative == collision

            if abs(r) < width and r < 0:
                self.num_batteries += 1
                if isinstance(closest, Battery):
                    batteries.remove(closest)
                    closest.kill()
            elif abs(l) < width and l < 0:
                self.num_batteries += 1
                if isinstance(closest, Battery):
                    batteries.remove(closest)
                    closest.kill()
            elif abs(b) < height and b < 0:
                self.num_batteries += 1
                if isinstance(closest, Battery):
                    batteries.remove(closest)
                    closest.kill()
            elif abs(t) < height and t < 0:
                self.num_batteries += 1
                if isinstance(closest, Battery):
                    batteries.remove(closest)
                    closest.kill()

    def door_check(self):
        hits = pygame.sprite.spritecollide(player, door_collision, False)
        if hits:
            closest = hits[0]
            width = closest.rect.right - closest.rect.left
            height = closest.rect.bottom - closest.rect.top
            r = closest.rect.left - self.rect.right # negative == collision
            l = self.rect.left - closest.rect.right # negative == collision
            b = closest.rect.top - self.rect.bottom # negative == collision
            t = self.rect.top - closest.rect.bottom # negative == collision

            if abs(r) < width and r < 0:
                return True
            elif abs(l) < width and l < 0:
                return True
            elif abs(b) < height and b < 0:
                return True
            elif abs(t) < height and t < 0:
                return True
            else:
                return False


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
            elif self.vel.x < 0:
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
    def dead_anim_update(self):
        if self.move_frame > 14:
            self.move_frame = 14
            return False
        self.image = self.explosion_anim[int(self.move_frame)]
        self.move_frame += 0.25
        return True

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
 
class Electricity(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.electricity_anim = [
            pygame.image.load("./res/electricity_01/0001.png"), pygame.image.load("./res/electricity_01/0002.png"), pygame.image.load("./res/electricity_01/0003.png"),
            pygame.image.load("./res/electricity_01/0004.png"), pygame.image.load("./res/electricity_01/0005.png"), pygame.image.load("./res/electricity_01/0006.png"),
            pygame.image.load("./res/electricity_01/0007.png"), pygame.image.load("./res/electricity_01/0008.png"), pygame.image.load("./res/electricity_01/0009.png"),
            pygame.image.load("./res/electricity_01/0010.png"), pygame.image.load("./res/electricity_01/0011.png"), pygame.image.load("./res/electricity_01/0012.png"),
            pygame.image.load("./res/electricity_01/0013.png"), pygame.image.load("./res/electricity_01/0014.png"), pygame.image.load("./res/electricity_01/0015.png"),
        ]
        self.image = pygame.transform.scale(self.electricity_anim[0], (150, 75))
        self.rect = pygame.Rect(position[0], position[1], self.image.get_width(), self.image.get_height())
        self.move_frame = 0

    def update(self):
        if self.move_frame > 14:
            self.move_frame = 0
            return
        self.image = pygame.transform.scale(self.electricity_anim[int(self.move_frame)], (150, 75))
        self.move_frame += 1

    def render(self):
        displaysurface.blit(self.image, (self.rect.x - camPos.x, self.rect.y - camPos.y))

class Battery(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("./res/battery.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
        self.rect = self.image.get_rect(center = position)

    def render(self):
        displaysurface.blit(self.image, (self.rect.x - camPos.x, self.rect.y - camPos.y))

class Door(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("./res/door.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
        self.rect = self.image.get_rect(center = position)

    def render(self):
        displaysurface.blit(self.image, (self.rect.x - camPos.x, self.rect.y - camPos.y))


background = Background("./res/background.png")
midground = Background("./res/midground.png")
midground.bgY = 20

ground = Ground()
player = Player()
platforms = [
    Platform((560, 170)), Platform((650, 40)), Platform((900, 30)),
    Platform((1050, 150)), Platform((1025, -150)), Platform((1200, 0)),
    Platform((1350, -75)), Platform((1460, -75))]
obstacles = [Electricity((705, 20))]
batteries = [Battery((650, -40)), Battery((1050, 70)), Battery((1025, -230))]

exitDoor = Door((1460, -150))
exitDoor.rect.center = (1460, -75 - exitDoor.image.get_height()/2)
door_collision = pygame.sprite.Group()
door_collision.add(exitDoor)


battery_icon = Battery((32, 36))
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('x'+str(player.num_batteries), True, (255,255,255))
textRect = text.get_rect()
textRect.center = (75,36)

collision_group = pygame.sprite.Group()
collision_group.add(ground)
for current_platform in platforms:
    collision_group.add(current_platform)

obstacle_group = pygame.sprite.Group()
for current_obstacle in obstacles:
    obstacle_group.add(current_obstacle)

battery_group = pygame.sprite.Group()
for current_battery in batteries:
    battery_group.add(current_battery)

offset1 = -5;
offset2 = -5;

playing = True
levelOver = False
while playing:
    platforms[2].rect.y += offset1
    if platforms[2].rect.y < -50 or platforms[2].rect.y > 110:
        offset1 *= -1

    # platforms[7].rect.x += offset2
    # if platforms[7].rect.x < 1440 or platforms[7].rect.x > 200000:
    #     offset2 *= -1

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
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()

    # update player

    if player.dead != True:
        player.update()
        # player.dead_anim_update()
        player.move()
        player.gravity_check()
        levelOver = player.door_check()
        player.battery_check()
        player.obst_check()
    else:
        playing = player.dead_anim_update()

    camPos = player.pos - vec(WIDTH/2, HEIGHT/2)

    r = platforms[0].rect.left - player.rect.right # negative == collision
    l = player.rect.left - platforms[0].rect.right 
    print(r)
    print(l)


    # Render Functions ------
    background.render()
    displaysurface.blit(midground.bgimage, (midground.bgX - camPos.x/3, midground.bgY - camPos.y/3))
    # midground.render()
    ground.render()
    exitDoor.render()
    for current_platform in platforms:
        current_platform.render()
    for current_obstacle in obstacles:
        current_obstacle.update()
        current_obstacle.render()
    for current_battery in batteries:
        current_battery.render()
    displaysurface.blit(player.image, (WIDTH/2 - player.image.get_width()/2, HEIGHT/2 - player.image.get_height()))

    # pygame.draw.rect(displaysurface, (255,0,0), pygame.Rect(obstacles[0].rect.x - camPos.x, obstacles[0].rect.y - camPos.y, obstacles[0].rect.width, obstacles[0].rect.height))


    text = font.render('x'+str(player.num_batteries), True, (255,255,255))
    displaysurface.blit(battery_icon.image, battery_icon.rect)
    displaysurface.blit(text, textRect)

    if levelOver:
        levelOverText = font.render('You Won!', True, (255,255,255))
        levelOverTextRect = text.get_rect()
        levelOverTextRect.center = (WIDTH/2 - levelOverTextRect.width*2, HEIGHT/2 - levelOverTextRect.height*5)

        f = open("saveFile.txt", "r")
        highscore = int(f.read())
        f.close()

        if player.num_batteries > highscore:
            f = open("saveFile.txt", "w")
            f.write(str(player.num_batteries))
            f.close()

        highscoreText = font.render('High Score: ' + str(highscore), True, (255,255,255))
        highscoreTextRect = highscoreText.get_rect()
        highscoreTextRect.center = (WIDTH/2, HEIGHT/3 + highscoreTextRect.height*2)

        score = font.render('Score: ' + str(player.num_batteries), True, (255,255,255))
        scoreTextRect = score.get_rect()
        scoreTextRect.center = (WIDTH/2, HEIGHT/3 + scoreTextRect.height)

        NextLvl = font.render('Next Level', True, (255,255,255), (255,0,0))
        NextLvlRect = score.get_rect()
        NextLvlRect.center = (WIDTH/2 - 25, HEIGHT/1.5 + NextLvlRect.height)

        pygame.draw.rect(displaysurface, (150,150,150), pygame.Rect(WIDTH*9/32, HEIGHT/16, WIDTH*7/16, HEIGHT*14/16))
        displaysurface.blit(levelOverText, levelOverTextRect)
        displaysurface.blit(highscoreText, highscoreTextRect)
        displaysurface.blit(NextLvl, NextLvlRect)
        displaysurface.blit(score, scoreTextRect)

    pygame.display.update() 
    FPS_CLOCK.tick(FPS)


gameOver = font.render('Game Over!', True, (255,255,255))
gameOverTextRect = text.get_rect()
gameOverTextRect.center = (WIDTH/2 - gameOverTextRect.width*2, HEIGHT/2 - gameOverTextRect.height*5)

f = open("saveFile.txt", "r")
highscore = int(f.read())
f.close()

if player.num_batteries > highscore:
    f = open("saveFile.txt", "w")
    f.write(str(player.num_batteries))
    f.close()

highscoreText = font.render('High Score: ' + str(highscore), True, (255,255,255))
highscoreTextRect = highscoreText.get_rect()
highscoreTextRect.center = (WIDTH/2, HEIGHT/2 + highscoreTextRect.height*2)

score = font.render('Score: ' + str(player.num_batteries), True, (255,255,255))
scoreTextRect = score.get_rect()
scoreTextRect.center = (WIDTH/2, HEIGHT/2 + scoreTextRect.height)

while True:
    for event in pygame.event.get():
        # Will run when the close window button is clicked    
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit() 
    pygame.draw.rect(displaysurface, (150,150,150), pygame.Rect(WIDTH*9/32, HEIGHT/16, WIDTH*7/16, HEIGHT*14/16))
    gameOver = font.render('Game Over!', True, (255,255,255))
    displaysurface.blit(gameOver, gameOverTextRect)
    displaysurface.blit(highscoreText, highscoreTextRect)
    displaysurface.blit(score, scoreTextRect)
    pygame.display.update()

