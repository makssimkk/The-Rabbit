from pygame import *
from config import BLOCK_WIDTH, BLOCK_HEIGHT


class Block(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image = image.load("blocks/ground1-5.png")
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT) #область для отслеживания пересечений блоков