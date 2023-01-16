from pygame import *
from config import *
import pyganim # для анимации нескольких картинок движения кролика
from block import BlockDie, BlockCarrot, Nora
from monster import Monster


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x_movement_speed = 0  # x_movement - скорость горизонтального перемещения. 0 - стоять на месте
        self.startX = x  # Начальная точка кролика Х, возвращение после смерти ####НА ПЕРСПЕКТИВУ###
        self.startY = y  # Начальная точка кролика Y, возвращение после смерти
        self.y_movement_speed = 0  # скорость вертикального перемещения
        self.onGround = False  # по умолчанию кролик не знает а есть ли поверхность чтоб оттолкнуться
        self.image = Surface((WIDTH, HEIGHT))  # параметры квадрата кролика
        self.image.fill(Color(COLOR))  # заливаем фон цветом
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        self.lives = 3

        # Анимация движения вправо
        rabbit_anim = []
        for anim in ANIMATION_RIGHT:
            rabbit_anim.append((anim, ANIMATION_SPEED))  # кортеж добавляется один “кадр” анимации и количество
            # миллисекунд, в течение которых оно отображается перед отображением следующего кадра
        self.rabbit_animRight = pyganim.PygAnimation(
            rabbit_anim)  # передаем кортедж изображений и время задержки анимации
        self.rabbit_animRight.play()  # проигрываем получившеюся последовательность

        # Анимация движения влево
        rabbit_anim = []
        for anim in ANIMATION_LEFT:
            rabbit_anim.append((anim, ANIMATION_SPEED))
        self.rabbit_animLeft = pyganim.PygAnimation(rabbit_anim)
        self.rabbit_animLeft.play()

        # Анимация стоящегог кролика
        self.rabbit_animStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.rabbit_animStay.play()
        self.rabbit_animStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        # Анимация кролика прыжка при нажатии лево вверх
        rabbit_anim = []
        for anim in ANIMATION_JUMP_LEFT:
            rabbit_anim.append((anim, ANIMATION_SPEED))
        self.rabbit_animJumpLeft = pyganim.PygAnimation(rabbit_anim)
        self.rabbit_animJumpLeft.play()

        # Анимация кролика прыжка при нажатии право вверх
        rabbit_anim = []
        for anim in ANIMATION_JUMP_RIGHT:
            rabbit_anim.append((anim, ANIMATION_SPEED))
        self.rabbit_animJumpRight = pyganim.PygAnimation(rabbit_anim)
        self.rabbit_animJumpRight.play()

        # Анимация кролика прыжок на месте
        self.rabbit_animJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.rabbit_animJump.play()

        # счетчик
        self.n_carrot = 0

        self.died = False  # пока не дошел до пня

    def update(self, left, right, up, blocks):  # обновляем право, лево, вверх, блоки

        if up:  # движение вверх
            if self.onGround:  # если есть поверхность от которой можно оттолкнуться прыгает
                self.y_movement_speed = -JUMP_POWER  # скорость вертикального  перемещения =силе прыжка жвижется вверх
            self.image.fill(Color(COLOR))  # заливаем
            self.rabbit_animJump.blit(self.image, (0, 0))  # накладываем картинку прыжка на поверхность на которой
            # отрисовываем и координаты левого верхнего угла

        if left:  # движение влево
            self.x_movement_speed = -MOVE_SPEED  # Лево  скорость горизонтального перемещения = x- n
            self.image.fill(Color(COLOR))
            if up:  # для прыжка влево
                self.rabbit_animJumpLeft.blit(self.image, (0, 0))
            else:
                self.rabbit_animLeft.blit(self.image, (0, 0))

        if right:  # движение враво
            self.x_movement_speed = MOVE_SPEED  # Скорость горизонтального перемещения тк вправо  = x + n
            self.image.fill(Color(COLOR))
            if up:  # если добавляется прыжок
                self.rabbit_animJumpRight.blit(self.image, (0, 0))
            else:
                self.rabbit_animRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти прааво или лево
            self.x_movement_speed = 0  # скорость горизонтального перемещения 0
            if not up:
                self.image.fill(Color(COLOR))
                self.rabbit_animStay.blit(self.image, (0, 0))

        if not self.onGround:  # если поверхности нет
            self.y_movement_speed += GRAVITY  # к вертикальной координате перемещения добавляю гравитацию

        self.onGround = False  # не известно когда есть поверхность для отталкивания
        self.rect.y += self.y_movement_speed
        self.collide(0, self.y_movement_speed, blocks)

        self.rect.x += self.x_movement_speed  # переносим свои положение на скорость перемещения по горизонтали
        self.collide(self.x_movement_speed, 0, blocks)

    def collide(self, x_movement_speed, y_movement_speed,
                blocks):  # проверка на пересечение координат героя и платформ,
        # если таковое имеется, то  происходит действие.
        for p in blocks:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if isinstance(p, BlockDie) or isinstance(p, Monster):  # если пересакаемый блок - blocks.BlockDie или Monster
                    if not self.died:
                        self.died = True
                        self.x_movement_speed = 0
                        self.y_movement_speed = 0
                        self.lives -= 1
                        if self.lives < 1:
                            self.game_over()
                        else:
                            self.die()  # смерть


                elif isinstance(p, Nora):  # если коснулись норы
                    # победили!!!
                    #show_winning()
                    pygame.event.post(pygame.event.Event(WIN_EVENT))
                    self.delete() # убираю героя иначе при перезапуски будет наложение картинки


                elif isinstance(p, BlockCarrot):  # если пересакаемый блок - шипы
                    self.n_carrot += 1
                    blocks.remove(p)
                    p.delete()


                else:
                    if x_movement_speed > 0:  # если движется вправо
                        self.rect.right = p.rect.left  # пеерсечение правой стороны игрока и платформы слева - не движится
                        # вправо

                    if x_movement_speed < 0:  # если движется влево
                        self.rect.left = p.rect.right  # пеерсечение левой стороны игрока и платформы справа - не движится
                        # влево

                    if y_movement_speed > 0:  # если падает вниз
                        self.rect.bottom = p.rect.top  # пеерсечение нижней стороны игрока и платформы сверху
                        self.onGround = True  # и становится на что-то твердое
                        self.y_movement_speed = 0  # и энергия падения пропадает

                    if y_movement_speed < 0:  # если движется вверх
                        self.rect.top = p.rect.bottom  # пеерсечение верхней стороны игрока и платформы снизу
                        self.y_movement_speed = 0  # и энергия прыжка пропадает

    def die(self):
        pygame.event.clear()
        self.n_carrot = 0
        pygame.event.post(pygame.event.Event(DIE_EVENT))

    def game_over(self):
        pygame.event.clear()
        self.n_carrot = 0
        pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def restore_lives(self):
        self.lives = 3

    def delete(self):
        self.kill()

