""" Scene """
import pygame


class Scene:
    """ Scene class, used to make scenes """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_scene = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(None, 24)
        self.persist = {}

    def startup(self, persist):
        """ pass a dict between scenes to persist data """
        self.persist = persist

    def get_event(self, event):
        """ handle a single event """
        raise NotImplementedError("you must define a *get_event()*")

    def update(self, dt):
        """ update the state called once per frame(dt) """
        raise NotImplementedError("you must define a *update()*")

    def draw(self, surface):
        """ draw the screen """
        raise NotImplementedError("you must define a *draw()*")
