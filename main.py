import pygame 
import os

pygame.init()
WIDTH, HEIGHT = 800, 500
pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hangman 2.O!")

limitf = 60
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(limitf)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()