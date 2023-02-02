# импортируем pygame
from pygame import *
# импортируем значения по умолчанию
from config import BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_COLOR


# класс простого блока
# все остальные блоки наследуем от него
class Block(sprite.Sprite):
    # инициализация
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image = image.load("blocks/ground1-5.png")
        self.image.set_colorkey(Color(BLOCK_COLOR))  # делаем фон прозрачным
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)  # область для отслеживания пересечений блоков


# класс блока смерти
# (меняем только картинку)
class BlockDie(Block):  # кристал-смерти
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load('blocks/Red Crystal Cluster-1.png')


# класс блока морковки
class BlockCarrot(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load('blocks/carrot.png')

    # удалить морковку
    def delete(self):
        self.kill()


# нора
class Nora(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load("Finish/TREE_HOUSE5-1.png")


# блок сердца
class BlockHeart(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load('blocks/life.png')

    def delete(self):
        self.kill()



