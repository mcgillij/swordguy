""" dorf class """
import pygame


class Dorf(pygame.sprite.Sprite):
    """ Dorf class """

    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.image = image
        self.rect = rect
        self.shooting = False

    def move_left(self):
        """ Move left """
        self.rect.x -= self.speed

    def move_right(self):
        """ Move right """
        self.rect.x += self.speed

    def move_up(self):
        """ Move up """
        self.rect.y -= self.speed

    def move_down(self):
        """ Move down """
        self.rect.y += self.speed
