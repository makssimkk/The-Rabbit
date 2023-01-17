from pygame import *
from config import BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_COLOR


class Block(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image = image.load("blocks/ground1-5.png")
        self.image.set_colorkey(Color(BLOCK_COLOR))  # делаем фон прозрачным
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)  # область для отслеживания пересечений блоков


class BlockDie(Block):  # кристал-смерти
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load('blocks/Red Crystal Cluster-1.png')


class BlockCarrot(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load('blocks/carrot.png')

    def delete(self):
        self.kill()


class Nora(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load("Finish/TREE_HOUSE5-1.png")


class BlockHeart(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load('blocks/life.png')

    def delete(self):
        self.kill()



