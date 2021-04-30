""" SceneManager class """
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


class SceneManager:
    """ used as the main state machine """
    def __init__(self, screen, scenes, starting_scene):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.scenes = scenes
        self.scene_name = starting_scene
        self.scene = self.scenes[self.scene_name]

    def event_loop(self):
        """ events are passed for the current scene """
        for event in pygame.event.get():
            self.scene.get_event(event)

    def next_scene(self):
        """ switch to the next scene """
        # current_scene = self.scene_name  # in the event we need to go back
        next_scene = self.scene.next_scene
        self.scene.done = False
        self.scene_name = next_scene
        persist = self.scene.persist
        self.scene = self.scenes[self.scene_name]
        self.scene.startup(persist)
        print("Am I getting called")
        print(self.scene.persist)

    def update(self, dt):
        """ checks if there's a scene change, and update """

        if self.scene.quit:
            self.done = True
        elif self.scene.done:
            self.next_scene()
        self.scene.update(dt)

    def draw(self):
        """ pass display to active scene for drawing """
        self.scene.draw(self.screen)

    def run(self):
        """ Main while 1 loop """
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()
