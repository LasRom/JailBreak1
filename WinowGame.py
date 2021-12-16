import os
import sys

import pygame

pygame.init()
size = width, height = 1000, 700
FPS = 60
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


clock = pygame.time.Clock()
x = 0
y = 0
running = True
while running:
    screen.fill([255, 255, 255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if x - 10 >= 0:
                    x -= 10
                    screen.blit(load_image('beg_zakl.png'), (x, y))
            if event.key == pygame.K_RIGHT:
                x += 10
                screen.blit(load_image('beg_zakl.png'), (x, y))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x - 10 >= 0:
                    x -= 10
                    screen.blit(load_image('beg_zakl.png'), (x, y))
            if event.key == pygame.K_RIGHT:
                x += 10
                screen.blit(load_image('beg_zakl.png'), (x, y))

    pygame.display.flip()

pygame.quit()
