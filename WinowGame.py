import os
import sys

import pygame

pygame.init()
size = width, height = 1000, 700
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

class Player(pygame.sprite.Sprite):
    image = load_image("stop_zakl.png")
    image_right = load_image("beg_zakl.png")
    image_stop = load_image("stop_zakl.png")
    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 620

    def update(self):
        if up:
            if self.rect.y - 6 > 0:
                self.rect.y -= 6
        elif right:
            if self.rect.x + 6 < 965:
                self.image = self.image_right
                self.rect.x += 6
        elif left:
            if self.rect.x - 6 >= 0:
                self.rect.x -= 6
        else:
            self.image = self.image_stop

up = False
left = False
right = False
player_sprites = pygame.sprite.Group()
Player(player_sprites)

RUN = True
FPS = 60
clock = pygame.time.Clock()


while RUN:
    clock.tick(FPS)
    for e in pygame.event.get():  # Обрабатываем события
        if e.type == pygame.QUIT:
            RUN = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
            up = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            left = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            right = True

        if e.type == pygame.KEYUP and e.key == pygame.K_UP:
            up = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
            right = False
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
            left = False
    screen.fill([255, 255, 255])
    player_sprites.draw(screen)
    player_sprites.update()
    pygame.display.flip()

pygame.quit()
