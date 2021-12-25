import os
import sys

import pygame
from pygame import *

pygame.init()
size = width, height = 992, 704  # размеры окна
screen = pygame.display.set_mode(size)  # холст
UP = False  # проверка на движение вверх
LEFT = False  # проверка движения в лево
RIGHT = False  # проверка движения в право
DOWN = False  # проверка движения в низ
HERO = None
PLATFORM_WIDTH = 32  # размеры платформы и лестницы
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (128, 128, 128)  # цвет платформы
STAIRS_COLOR = (255, 0, 0)
DOOR_COLOR = (0, 0, 255)
FPS = 60  # кол-во кадров
clock = pygame.time.Clock()

# все спрайты
all_sprites = pygame.sprite.Group()  # Все объекты
platforms = pygame.sprite.Group()
hero_sprite = pygame.sprite.Group()
stairs_sprite = pygame.sprite.Group()
platforms_and_stairs = pygame.sprite.Group()
door_sprite = pygame.sprite.Group()
policemen_sprite = pygame.sprite.Group()


# функция которая завершает работу
def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


# создаем задний фон
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BackGround = Background('data/fon.png', [0, 0])


class Player(pygame.sprite.Sprite):
    image = load_image("stop_zakl.png")
    image_right = load_image("beg_zakl.png")
    image_stop = load_image("stop_zakl.png")

    def __init__(self, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(all_sprites)
        self.image = Player.image
        self.speed = 3
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.flag_g = True  # если в воздухе
        self.flag_st = False  # если на лестнице
        # дальше идут доп проверки дабы исправить некоторые баги
        self.flag_st_dop = True

    def update(self):
        # проверяю не дошел ли герой до двери
        for el in door_sprite:
            if pygame.sprite.collide_mask(self, el):
                terminate()
        # проверяю не в воздухе ли персонаж
        for el in platforms_and_stairs:
            if not pygame.sprite.collide_mask(self, el):
                self.flag_g = True
            else:
                self.flag_g = False
                break
        # если в воздухе то он равномерно падает
        if self.flag_g:
            self.rect = self.rect.move(0, 3)
        # проверка стоит ли на лестнице персонаж
        for el in stairs_sprite:
            if not pygame.sprite.collide_mask(self, el):
                self.flag_st = False
            else:
                self.flag_st = True
                break
        # доп проверка для исправления одного из багов(игрок при спуске по лестнице проваливался в платформу)
        for el in platforms:
            if pygame.sprite.collide_mask(self, el):
                self.flag_st_dop = False
                break
            else:
                self.flag_st_dop = True
        # движение вверх, вправо, влево, вниз
        if UP and self.flag_st:
            self.rect.y -= 5
            self.image = self.image_stop
        if RIGHT and self.rect.x + self.speed < width - 70:
            self.image = self.image_right
            self.rect.x += self.speed
        if LEFT and self.rect.x - self.speed > 33:
            self.rect.x -= self.speed
            self.image = self.image_stop
        if DOWN and self.flag_st and self.flag_st_dop:
            self.rect.y += self.speed
            self.image = self.image_stop
        if not (LEFT and UP and RIGHT and DOWN):
            self.image = self.image_stop


# временный  уровень
def load_level(filename):
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


level = load_level('level_1.txt')  # считываем уровень
print(level)


class Platform(pygame.sprite.Sprite):
    image_stairs = load_image("Лестница.png")

    def __init__(self, x, y, plat="стена"):
        super().__init__(all_sprites)
        if plat == "стена":
            self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image.fill(Color(PLATFORM_COLOR))
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            self.mask = pygame.mask.from_surface(self.image)
        elif plat == "лестница":
            self.image = Platform.image_stairs
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            self.mask = pygame.mask.from_surface(self.image)
        elif plat == "дверь":
            self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image.fill(Color(DOOR_COLOR))
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            self.mask = pygame.mask.from_surface(self.image)


class Creat_Police(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)
        self.flag = True

    def update(self):
        for el in hero_sprite:
            if pygame.sprite.collide_mask(self, el):
                terminate()
        if self.x + 3 > width - 70:
            self.flag = False
        elif self.x - 3 < 32:
            self.flag = True
        if self.flag:
            self.x += 1.5
            self.rect = Rect(int(self.x), self.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        else:
            self.x -= 1.5
            self.rect = Rect(int(self.x), self.y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


x = y = 0
for row in level:  # вся строка
    for col in row:  # каждый символ
        if col == "-":
            pf = Platform(x, y)
            all_sprites.add(pf)
            platforms.add(pf)
            platforms_and_stairs.add(pf)
        elif col == "+":
            pf = Platform(x, y, plat="лестница")
            all_sprites.add(pf)
            stairs_sprite.add(pf)
            platforms_and_stairs.add(pf)
        elif col == "D":
            pf = Platform(x, y, plat="дверь")
            all_sprites.add(pf)
            door_sprite.add(pf)
        elif col == "P":
            pol = Creat_Police(x, y)
            policemen_sprite.add(pol)
        elif col == "H":
            hero = Player(x, y)
            hero_sprite.add(hero)
            HERO = hero
        x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
    y += PLATFORM_HEIGHT  # то же самое и с высотой
    x = 0  # на каждой новой строчке начинаем с нуля

# добавляю игрока во все спрайты в конце чтобы он не пропадал за платформами
RUN = True
while RUN:
    screen.fill([255, 255, 255])
    clock.tick(FPS)
    for e in pygame.event.get():  # Обрабатываем события
        if e.type == pygame.QUIT:
            RUN = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            LEFT = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            RIGHT = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
            DOWN = True
        if e.type == KEYDOWN and e.key == K_UP:
            UP = True

        if e.type == KEYUP and e.key == K_UP:
            UP = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
            RIGHT = False
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
            LEFT = False
        if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
            DOWN = False
    screen.blit(BackGround.image, BackGround.rect)
    all_sprites.draw(screen)
    all_sprites.update()
    policemen_sprite.draw(screen)
    policemen_sprite.update()
    hero_sprite.draw(screen)
    hero_sprite.update()
    pygame.display.flip()

pygame.quit()
