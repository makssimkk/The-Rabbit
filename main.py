# импортируем библиотеки
from os import path
from pygame import *

# импортируем классы из других файлов
from config import *
from player import Player
from camera import Camera, camera_configure
from block import Block, BlockDie, BlockCarrot, Nora, BlockHeart
from monster import Monster
from button import Button


# главный класс с самой игрой
class Game:
    # инициализация
    def __init__(self):

        self.screen = pygame.display.set_mode(WINDOW)  # Создаем окошко
        pygame.display.set_caption("Crazy Rabbit")  # Пишем название в шапку
        self.backgrounds = [pygame.image.load('blocks/bg1.jpg'), pygame.image.load('blocks/bg2.jpg'),
                            pygame.image.load('blocks/bg3.jpg')]
        pygame.mixer.music.load('Music/Jungle trail bpm90 C Example Background.wav')  # мелодия игры
        pygame.mixer.music.set_volume(0.4)  # громкость мелодии
        pygame.mixer.music.play(loops=-1)  # зациклила мелодию

        # создаем уменьшенное изображение для отображения жизней
        player_img = pygame.image.load(path.join('img/r4-1.png')).convert()
        self.player_mini_img = pygame.transform.scale(player_img, (25, 19))
        self.player_mini_img.set_colorkey(Color(0, 0, 0))  # Black

        # координаты игрока
        self.playerX = 0
        self.playerY = 0

        self.all_objects = pygame.sprite.Group()  # Все объекты
        self.blocks = []  # то, во что мы будем врезаться или опираться

        self.monsters = pygame.sprite.Group()  # Все передвигающиеся объекты

        # текущий уровень
        self.current_level = 1
        self.level = []
        # загружаем уровень
        self.load_level(self.current_level)

        total_level_width = len(
            self.level[0]) * BLOCK_WIDTH  # Создаем большой прямоугольник уровня. Это дляя камеры Высчитываем
        # фактическую  ширину уровня
        total_level_height = len(self.level) * BLOCK_HEIGHT  # высоту

        # инициализируем кролика
        self.hero = Player(self.playerX, self.playerY)  # начальная создаем героя по (x,y) координатам
        self.left = self.right = False  # по умолчанию - стоим
        self.up = False

        # в список со всеми объектами добавляем кролика
        self.all_objects.add(self.hero)
        self.timer = pygame.time.Clock()

        # иниацилизируем камеру
        self.camera = Camera(camera_configure, total_level_width, total_level_height)
        self.running = True
        self.game_over = False
        self.waiting_win = False
        self.main_menu = True

    # метод загрузки уровня
    def load_level(self, num_level):
        # по переданому числу, загружаем нужный уровень
        # уровни хранятся в файлах
        level_file = open(f'levels/{num_level}.txt')
        line = " "
        self.level.clear()
        # работа с файлом уровня
        while line[0] != "/":  # пока не нашли символ завершения файла
            line = level_file.readline()  # считываем построчно
            if line[0] == "[":  # если нашли символ начала уровня
                while line[0] != "]":  # то, пока не нашли символ конца уровня
                    line = level_file.readline()  # считываем построчно уровень
                    if line[0] != "]":  # и если нет символа конца уровня
                        endLine = line.find("|")  # то ищем символ конца строки
                        self.level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"

            if line[0] != "":  # если строка не пустая
                commands = line.split()  # разбиваем ее на отдельные команды
                if len(commands) > 1:  # если количество команд > 1, то ищем эти команды

                    if commands[0] == "player":  # если первая команда - player
                        self.playerX = int(commands[1])  # то записываем координаты героя
                        self.playerY = int(commands[2])

                    if commands[0] == "monster":  # если первая команда monster, то создаем монстра
                        mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                     int(commands[5]), int(commands[6]))
                        self.all_objects.add(mn)
                        self.blocks.append(mn)
                        self.monsters.add(mn)

    # метод отрисовки уровня
    def draw_level(self):
        x = y = 0  # координаты
        for row in self.level:  # вся строка
            for col in row:  # каждый символ
                # блоки
                if col == "-":
                    pf = Block(x, y)
                    self.all_objects.add(pf)
                    self.blocks.append(pf)
                # шипы
                if col == "d":
                    bd = BlockDie(x, y)
                    self.all_objects.add(bd)
                    self.blocks.append(bd)
                # нора
                if col == 'N':
                    bn = Nora(x, y)
                    self.all_objects.add(bn)
                    self.blocks.append(bn)
                # морковка
                if col == "c":
                    bc = BlockCarrot(x, y)
                    self.all_objects.add(bc)
                    self.blocks.append(bc)
                # сердце, прибавляющее дополнительную жизнь
                if col == "h":
                    bc = BlockHeart(x, y)
                    self.all_objects.add(bc)
                    self.blocks.append(bc)

                x += BLOCK_WIDTH  # блоки платформы ставятся на ширине блоков
            y += BLOCK_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

    # метод перезапуска уровня
    # (запуск при смерти)
    def restart_level(self):
        pygame.mixer.music.unpause()
        self.up = False
        self.left = self.right = False
        self.blocks.clear()
        self.all_objects.empty()
        self.all_objects.add(self.hero)
        self.load_level(self.current_level)
        self.draw_level()
        self.hero.died = False
        self.hero.teleporting(self.hero.startX, self.hero.startY)

    # метод переключения уровня
    def next_level(self):
        self.current_level += 1
        # если пройден 3 уровень, то возвращаем на 1
        if self.current_level > MAX_LEVEL:
            self.current_level = 1
            self.waiting_win = True
            self.show_winning()
        self.restart_level()

    # метод перезапуска игры
    # (запуск при потере всех жизней)
    def reset_game(self):
        self.game_over = True
        # возврат на 1 уровень
        self.current_level = 1
        self.restart_level()
        self.hero.restore_lives()

    # обработка событий
    def listen_event(self):
        for event in pygame.event.get():  # Обрабатываем события кнопок
            if event.type == QUIT:
                self.running = False
            # при проигранной игре (потере всех жизней)
            if event.type == GAME_OVER_EVENT:
                self.reset_game()
            # при смерти
            if event.type == DIE_EVENT:
                self.restart_level()
            # при победе
            if event.type == WIN_EVENT:
                self.next_level()
            # обработка кнопок
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

    # метод для обработки кадра
    def tick(self):
        self.timer.tick(60)
        self.screen.blit(self.backgrounds[self.current_level - 1], (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        self.camera.update(self.hero)  # центризируем камеру относительно персонажа
        self.monsters.update(self.blocks)  # обновляем переносим блоки
        self.hero.update(self.left, self.right, self.up, self.blocks)  # передвижение
        # all_objects.draw(screen) # отображение
        for event in self.all_objects: #меньший прямоугольник  равны размеру окна цетрирующийся относительно главного героя и
            # где прорисовываются все объекты
            self.screen.blit(event.image, self.camera.apply(event)) # Каждую итерацию необходимо всё перерисовывать под положение
            # камеры относительно главного героя
        self.draw_lives(80, 10, self.hero.lives, self.player_mini_img)  # прорисовка колличства жизни кроликами

    # счетчик
    def counter(self):
        # работа со счетчиком
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(str(self.hero.n_carrot), True, (255, 255, 255))
        self.screen.blit(text1, (10, 10))
        # картинка морковки рядом с счетчиком
        img = pygame.image.load("blocks/carrot.png")
        self.screen.blit(img, (27, 0))

    # заставка при проигрыше
    def show_go_screen(self):
        # ставим музыку на паузу
        pygame.mixer.music.pause()
        # поле game over
        background = pygame.image.load('game over/game over3 500-800.jpg.png')
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.game_over = False
                    self.main_menu = True

        pygame.event.clear()
        self.restart_level()

    # заставка при выигрыше
    def show_winning(self):
        # ставим музыку на паузу
        pygame.mixer.music.pause()
        # win/continue
        bg = pygame.image.load('you win/заставка800-500.png')
        self.screen.blit(bg, (0, 0))
        pygame.display.flip()

        while self.waiting_win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.waiting_win = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.waiting_win = False
                    self.main_menu = True

        pygame.event.clear()
        self.restart_level()
        self.hero.lives = 3

    # отрисовка жизней (мини-кроликов в углу экрана)
    def draw_lives(self, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            self.screen.blit(img, img_rect)

    # заставка главного меню
    def show_main_menu(self):
        # ставим музыку на паузу
        pygame.mixer.music.pause()
        # start menu
        bg = pygame.image.load('menu/main_menu1.jpg')
        self.screen.blit(bg, (0, 0))

        mouse_handlers = []
        buttons = []
        # отрисовка кнопок
        for i, (text, click_handler) in enumerate((('PLAY', self.play), ('QUIT', self.exit))):
            b = Button(MENU_OFFSET_X,
                       MENU_OFFSET_Y + (MENU_BUTTON_H + 15) * i,
                       MENU_BUTTON_W,
                       MENU_BUTTON_H,
                       text,
                       click_handler,
                       padding=15)
            b.draw(self.screen)
            mouse_handlers.append(b.handle_mouse_event)
            buttons.append(b)

        pygame.display.flip()

        # отслеживание событий мыши
        while self.main_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_menu = False
                    self.running = False
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    for handler in mouse_handlers:
                        handler(event.type, event.pos)

            for b in buttons:
                b.draw(self.screen)

            pygame.display.update()
            self.timer.tick(60)

    # выход из игры
    def exit(self, button):
        self.main_menu = False
        self.running = False

    # запуск игры
    def play(self, button):
        self.main_menu = False
        pygame.mixer.music.unpause()

    # Основной цикл программы
    def run(self):
        while self.running:
            # если мы в главном меню
            if self.main_menu:
                self.show_main_menu()

            # если игра закончилась
            if self.game_over:
                self.show_go_screen()

            # подключаем функцию ожидания для этого состояния или крестик и выход или перезапуск
            if self.waiting_win:
                self.show_winning()

            self.listen_event()
            self.tick()
            self.counter()
            pygame.display.update()  # обновление и вывод всех изменений на экранн


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    # инициализация игры
    game = Game()
    # отрисовываем уровень
    game.draw_level()
    # запускаем игру
    game.run()


if __name__ == '__main__':
    main()