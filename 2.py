import sys
import pygame

pygame.init()
size=width, height = 640, 480
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size)

rocket = pygame.image.load("rocket.png")
metiorites = pygame.image.load("meteor.png")

rocrect = rocket.get_rect()
metrect = metiorites.get_rect()

rocrect.size = (32, 32)
metrect.size = (32, 32)

screen.fill(black)
screen.blit(rocket, rocrect)
screen.blit(metiorites, metrect)

pygame.display.flip()

#rocrect = rocrect.move([0, height-20])
#keys = pygame.key.get_pressed()
#if keys[pygame.K_RIGHT]:
#        rocrect = rocrect.move([3,0])
#if keys[pygame.K_LEFT]:
#        rocrect = rocrect.move([-3,0])
