# импортируем библиотеки
from pygame import *
from config import *
# библиотека для анимации нескольких картинок движения кролика
import pyganim


# класс монстров
class Monster(sprite.Sprite):
    # инициализация
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))  # прозрачный слой
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.x_movement_speed = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.y_movement_speed = up  # скорость движения по вертикали, 0 - не двигается
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    # по принципу героя
    def update(self, blocks):
        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        # переносим свои положение на скорость перемещения по горизонтали и вертикали
        self.rect.y += self.y_movement_speed
        self.rect.x += self.x_movement_speed

        self.collide(blocks)

        # если прошли максимальное растояние, то идеи в обратную сторону горизонталь
        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.x_movement_speed = -self.x_movement_speed
        # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.y_movement_speed = -self.y_movement_speed

    # проверка на пересечение координат героя и платформ,
    # если таковое имеется, то  происходит действие.
    def collide(self, blocks):
        for p in blocks:
            # если с чем-то или кем-то столкнулись
            if sprite.collide_rect(self, p) and self != p:
                # то поворачиваем в обратную сторону
                self.x_movement_speed = - self.x_movement_speed
                self.y_movement_speed = - self.y_movement_speed

