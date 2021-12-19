import os
import sys

import pygame
from pygame import *

pygame.init()
size = width, height = 992, 704  # размеры окна
screen = pygame.display.set_mode(size)  # холст


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# создаем задний фон
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BackGround = Background('data/fon.png', [0, 0])

up = False  # проверка на движение вверх
left = False  # проверка движения в лево
right = False  # проверка движения в право
down = False  # проверка движения в низ

PLATFORM_WIDTH = 32  # размеры платформы
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (128, 128, 128)  # цвет платформы

all_sprites = pygame.sprite.Group()  # Все объекты
platforms = []  # то, во что мы будем врезаться или опираться


class Player(pygame.sprite.Sprite):
    image = load_image("stop_zakl.png")
    image_right = load_image("beg_zakl.png")
    image_stop = load_image("stop_zakl.png")

    def __init__(self):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if up:
            self.rect.y -= 5
            self.image = self.image_stop
        if right:
            self.image = self.image_right
            self.rect.x += 5
        if left:
            self.rect.x -= 5
            self.image = self.image_stop
        if down:
            self.rect.y += 5
            self.image = self.image_stop
        if not (left and up and right and down):
            self.image = self.image_stop

        if not pygame.sprite.collide_mask(self, pf):
            print(1, pf)
            self.rect = self.rect.move(0, 1)
        else:
            print(2)


# оздаем игрока
hero = Player()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)


# временный  уровень
level = [
    "-------------------------------",
    "                               ",
    "                               ",
    "                               ",
    "                               ",
    "-------  ----------------------",
    "                               ",
    "                               ",
    "                               ",
    "-------  ----------------------",
    "                               ",
    "                               ",
    "                               ",
    "-------  ----------------------",
    "                               ",
    "                               ",
    "                               ",
    "-------  ----------------------",
    "                               ",
    "                               ",
    "                               ",
    "-------------------------------"]
x = y = 0  # координаты
for row in level:  # вся строка
    for col in row:  # каждый символ
        if col == "-":
            pf = Platform(x, y)
            all_sprites.add(pf)
            platforms.append(pf)
        x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
    y += PLATFORM_HEIGHT  # то же самое и с высотой
    x = 0  # на каждой новой строчке начинаем с нуля
all_sprites.add(hero)

RUN = True
FPS = 60
clock = pygame.time.Clock()
while RUN:
    screen.fill([255, 255, 255])
    clock.tick(FPS)
    for e in pygame.event.get():  # Обрабатываем события
        if e.type == pygame.QUIT:
            RUN = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            left = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            right = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
            down = True
        if e.type == KEYDOWN and e.key == K_UP:
            up = True

        if e.type == KEYUP and e.key == K_UP:
            up = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
            right = False
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
            left = False
        if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
            down = False
    screen.blit(BackGround.image, BackGround.rect)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

pygame.quit()
