""" Utils """
import os
import pygame


def load_png(image_name):
    """ Load image and return image object and rect """
    fullname = os.path.join("data", image_name)

    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print("Cannot load image: ", fullname)
        raise SystemExit(message)
    return image, image.get_rect()


def load_image(image_name):
    """ Load image and return image object """
    fullname = os.path.join("data", image_name)

    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print("Cannot load image: ", fullname)
        raise SystemExit(message)
    return image
