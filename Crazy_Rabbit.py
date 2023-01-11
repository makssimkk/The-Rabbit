import pygame
from pygame import *
#import pygame_menu
#from pygame_menu import themes
from level_config import LEVEL
from config import *
from player import Player
from camera import Camera, camera_configure
from block import Block, BlockDie, BlockCarrot


class Game:
    def __init__(self):

        self.screen = pygame.display.set_mode(WINDOW)  # Создаем окошко
        pygame.display.set_caption("Crazy Rabbit")  # Пишем название в шапку
        self.background = pygame.image.load('blocks/background_3-1.jpg')

        self.hero = Player(40, 630)  # начальная создаем героя по (x,y) координатам
        self.left = self.right = False  # по умолчанию - стоим
        self.up = False

        self.all_objects = pygame.sprite.Group()  # Все объекты
        self.blocks = []  # то, во что мы будем врезаться или опираться

        self.all_objects.add(self.hero)
        self.timer = pygame.time.Clock()

        self.level = LEVEL

        total_level_width = len(
            self.level[0]) * BLOCK_WIDTH  # Создаем большой прямоугольник уровня. Это дляя камеры Высчитываем
        # фактическую  ширину уровня
        total_level_height = len(self.level) * BLOCK_HEIGHT  # высоту

        self.camera = Camera(camera_configure, total_level_width, total_level_height)
        self.running = True

    def draw_level(self):
        x = y = 0  # координаты
        for row in self.level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    pf = Block(x, y)
                    self.all_objects.add(pf)
                    self.blocks.append(pf)
                if col == "d":
                    bd = BlockDie(x, y)
                    self.all_objects.add(bd)
                    self.blocks.append(bd)

                if col == "c":
                    bc = BlockCarrot(x, y)
                    self.all_objects.add(bc)
                    self.blocks.append(bc)

                x += BLOCK_WIDTH  # блоки платформы ставятся на ширине блоков
            y += BLOCK_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

    def restart_level(self):
        self.up = False
        self.left = self.right = False
        self.blocks.clear()
        self.all_objects.empty()
        self.all_objects.add(self.hero)
        self.draw_level()
        self.hero.teleporting(self.hero.startX, self.hero.startY)

    def listen_event(self):
        for event in pygame.event.get():  # Обрабатываем события кнопок
            if event.type == QUIT:
                self.running = False
            if event.type == DIE_EVENT:
                self.restart_level()
            if event.type == KEYDOWN and event.key == K_UP:
                self.up = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.right = True

            if event.type == KEYUP and event.key == K_UP:
                self.up = False
            if event.type == KEYUP and event.key == K_RIGHT:
                self.right = False
            if event.type == KEYUP and event.key == K_LEFT:
                self.left = False

    def tick(self):
        self.timer.tick(60)
        self.screen.blit(self.background, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        self.camera.update(self.hero)  # центризируем камеру относительно персонажа
        self.hero.update(self.left, self.right, self.up, self.blocks)  # передвижение
        # all_objects.draw(screen) # отображение
        for event in self.all_objects: #меньший прямоугольник  равны размеру окна цетрирующийся относительно главного героя и
            # где прорисовываются все объекты
            self.screen.blit(event.image, self.camera.apply(event)) # Каждую итерацию необходимо всё перерисовывать под положение
            # камеры относительно главного героя

    def counter(self):
        # работа со счетчиком
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(str(self.hero.n_carrot), True, (255, 255, 255))
        self.screen.blit(text1, (10, 10))
        # картинка морковки рядом с счетчиком
        img = pygame.image.load("blocks/carrot.png")
        self.screen.blit(img, (27, 0))


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    game = Game()
    game.draw_level()

    while game.running:  # Основной цикл программы
        game.listen_event()
        game.tick()
        game.counter()
        pygame.display.update()  # обновление и вывод всех изменений на экранн


if __name__ == '__main__':
    main()
