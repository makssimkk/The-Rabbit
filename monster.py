from pygame import *
from config import *
import pyganim # для анимации нескольких картинок движения кролика


class Monster(sprite.Sprite):
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

    def update(self, blocks):  # по принципу героя

        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.y_movement_speed
        self.rect.x += self.x_movement_speed

        self.collide(blocks)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.x_movement_speed = -self.x_movement_speed  # если прошли максимальное растояние, то идеи в обратную сторону горизонталь
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.y_movement_speed = -self.y_movement_speed  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, blocks):
        for p in blocks:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.x_movement_speed = - self.x_movement_speed  # то поворачиваем в обратную сторону
                self.y_movement_speed = - self.y_movement_speed

