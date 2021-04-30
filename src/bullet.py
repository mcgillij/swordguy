""" bullet class """
import pygame
from utils import load_png


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self.size = 10
        self.speed = 10
        self.image = image
        self.rect = rect
