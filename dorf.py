""" dorf class """
import pygame
import pymunk.pygame_util
from pymunk import Vec2d

pymunk.pygame_util.positive_y_is_up = True


class Dorf(pygame.sprite.Sprite):
    """ Dorf class """

    def __init__(self, images, body):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.size = 10
        self.images = images
        self.image = images[0]
        self.rect = images[0].get_rect()
        self.shooting = False
        self.body = body

    def move_left(self):
        """ Move left """
        self.image = pygame.transform.flip(self.images[2], True, False)
        self.rect.x -= self.speed
        p = self.body.position
        p = Vec2d(p.x - self.speed, p.y)
        self.body.position = p

    def move_right(self):
        """ Move right """
        self.image = self.images[1]
        self.rect.x += self.speed
        p = self.body.position
        p = Vec2d(p.x + self.speed, p.y)
        self.body.position = p

    def move_up(self):
        """ Move up """
        self.rect.y -= self.speed
        p = self.body.position
        p = Vec2d(p.x, p.y - self.speed)
        self.body.position = p

    def move_down(self):
        """ Move down """
        self.rect.y += self.speed
        p = self.body.position
        p = Vec2d(p.x, p.y + self.speed)
        self.body.position = p
        self.image = pygame.transform.flip(self.images[2], False, True)
