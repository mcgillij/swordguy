""" dorf class """
import pygame


class Dorf(pygame.sprite.Sprite):
    """ Dorf class """

    def __init__(self, images):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.images = images
        self.image = images[0]
        self.rect = images[0].get_rect()
        self.shooting = False

    def move_left(self):
        """ Move left """
        self.image = self.images[1]
        self.rect.x -= self.speed

    def move_right(self):
        """ Move right """
        self.image = self.images[2]
        self.rect.x += self.speed

    def move_up(self):
        """ Move up """
        self.rect.y -= self.speed

    def move_down(self):
        """ Move down """
        self.rect.y += self.speed
