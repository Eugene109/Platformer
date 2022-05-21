import pygame as pygame
import math
import random
pygame.init()



WINDOW_WIDTH, WINDOW_HEIGHT = (500, 300)
#Initial Variables
WINDOW = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )

ball = pygame.Rect(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 10, 10)

player1 = pygame.Rect(20 - 3, WINDOW_HEIGHT/2 - 9, 6, 30)
player2 = pygame.Rect(WINDOW_WIDTH - 20 - 3, WINDOW_HEIGHT/2 - 9, 6, 30)

ballXVel = -1
ballYVel = 1

K_w, K_s, K_UP, K_DOWN = (0, 1, 2 , 3)
keysdown = [False, False, False, False]

def main():
    running = True
  
    global ballXVel
    global ballYVel
  
    clock = pygame.time.Clock()
  
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    keysdown[K_w] = True
                if event.key == pygame.K_s:
                    keysdown[K_s] = True
                if event.key == pygame.K_UP:
                    keysdown[K_UP] = True
                if event.key == pygame.K_DOWN:
                    keysdown[K_DOWN] = True
        print(keysdown)

        if ball.collidelist([player1, player2]) != -1:
            ballXVel *= -1

        if ball.y + 10 >= WINDOW_HEIGHT or ball.y <= 0:
            ballYVel *= -1

        if ball.x + 10 >= WINDOW_WIDTH or ball.x <= 0:
            ballXVel *= -1
        
        ball.x += ballXVel
        ball.y += ballYVel

        if keysdown[K_w]:
            player1.y -= 1
        if keysdown[K_s]:
            player1.y += 1
        if keysdown[K_UP]:
            player2.y -= 1
        if keysdown[K_DOWN]:
            player2.y += 1
    
        draw()

    pygame.quit()


def draw():
    WINDOW.fill( (255, 255, 255) )

    pygame.draw.rect(WINDOW, (0, 0, 0), ball)
    pygame.draw.rect(WINDOW, (0, 0, 0), player1)
    pygame.draw.rect(WINDOW, (0, 0, 0), player2)

    pygame.display.update()

if __name__ == "__main__":
    main()