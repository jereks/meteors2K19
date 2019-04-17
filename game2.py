import sys
import pygame

pygame.init()
size = width, height = 640, 480
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.gif")
platform = pygame.image.load("platform.png")

ballrect = ball.get_rect()
plrect = platform.get_rect()

plrect = plrect.move([0, height-20])

def collission():
    if plrect.x + plrect.size[0] >= ballrect.left >= plrect.x:
        if plrect.y >= ballrect.bottom >= plrect.y:
            return True

while True:

    if collission():
        speed[1] = - speed[1]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if plrect.right < width:
            plrect = plrect.move([3,0])
    if keys[pygame.K_LEFT]:
        if plrect.left > 0:
            plrect = plrect.move([-3,0])

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0:
        speed[1] = -speed[1]

    if ballrect.bottom > height:
        speed[1] = 0
        speed[0] = 0
        

        
    screen.fill(black)
    
    screen.blit(ball, ballrect)
    screen.blit(platform, plrect)

    pygame.time.wait(5)

    pygame.display.flip()

