""" scenes """

import pygame
from pygame.locals import *  # noqa: F401
from scenemanager import Scene
from inputmanager import InputManager


class StartupScene(Scene):
    def __init__(self):
        super().__init__()
        self.title = self.font.render("Startup Scene", True, pygame.Color("red"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = 'black'
        self.next_scene = "MAIN"
        self.inputmanager = InputManager()
        self.button_index = 0
        print("I'm in startup")

    def do_joystick_stuffs(self):
        num_joysticks = pygame.joystick.get_count()
        if num_joysticks < 1:
            print("You haven't plugged in any joysticks")
            return

    def get_event(self, event):
        is_configured = self.button_index >= len(self.inputmanager.buttons)
        if not is_configured:
            success = self.configure_phase(self.inputmanager.buttons[self.button_index])
            if success:
                self.button_index += 1
        else:
            # do interaction phase
            print("Doing interaction")

    def configure_phase(self, button):
        self.inputmanager.get_events()
        success = self.inputmanager.configure_button(button)
        print(f"Press the {button} button")
        return success

    def draw(self, surface):
        surface.fill(pygame.Color(self.persist['screen_color']))
        surface.blit(self.title, self.title_rect)

    def update(self, dt):
        pass



class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.title = self.font.render("MainScene", True, pygame.Color("blue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = 'black'
        self.next_scene = "OTHER"
        print("I'm in main")

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            self.persist['screen_color'] = "gold"
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color(self.persist['screen_color']))
        surface.blit(self.title, self.title_rect)

    def update(self, dt):
        pass

class OtherScene(Scene):
    def __init__(self):
        super().__init__()
        self.title = self.font.render("OTHER", True, pygame.Color("pink"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = 'black'
        self.next_scene = "STARTUP"
        print("I'm in other")

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            self.persist['screen_color'] = "brown"
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color(self.persist['screen_color']))
        surface.blit(self.title, self.title_rect)

    def update(self, dt):
        pass
