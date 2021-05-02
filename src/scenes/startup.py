""" Startup Scene """

import pygame
from pygame.locals import *  # noqa: F401
from .scene import Scene

cached_text = {}
cached_font = None


def write_text(screen, text, x, y):
    global cached_text, cached_font
    image = cached_text.get(text)
    if image is None:
        if cached_font is None:
            cached_font = pygame.font.Font(pygame.font.get_default_font(), 12)
        image = cached_font.render(text, True, (255, 255, 255))
        cached_text[text] = image
    screen.blit(image, (x, y - image.get_height()))


class StartupScene(Scene):
    def __init__(self):
        super().__init__()
        self.title = self.font.render("Startup Scene", True, pygame.Color("red"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = 'black'
        self.next_scene = "MAIN"
        self.inputmanager = None
        self.button_index = 0
        print("I'm in startup")
        self.configuration_message = ""

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
            # Try moving to main scene once joystick is configured
            print("Moving to other scene")
            self.done = True

    def configure_phase(self, button):
        success = self.inputmanager.configure_button(button)
        self.configuration_message = f"Press the {button} button"
        return success

    def draw(self, surface):
        surface.fill(pygame.Color(self.persist['screen_color']))
        surface.blit(self.title, self.title_rect)
        write_text(surface, self.configuration_message, 20, 20)

    def update(self, dt):
        pass
