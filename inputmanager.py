""" Input Manager """
import pygame
from pygame.locals import *


class InputEvent:
    def __init__(self, key, down):
        self.key = key
        self.down = down
        self.up = not down


class InputManager:
    def __init__(self):

        self.init_joystick()

        self.buttons = [
            "up",
            "down",
            "left",
            "right",
            "start",
            "A",
            "B",
            "X",
            "Y",
            "L",
            "R",
        ]
        # keyboard map
        self.key_map = {
            K_UP: "up",
            K_DOWN: "down",
            K_LEFT: "left",
            K_RIGHT: "right",
            K_RETURN: "start",
            K_a: "A",
            K_b: "B",
            K_x: "X",
            K_y: "Y",
            K_l: "L",
            K_r: "R",
        }
        # This dictionary will tell you which logical buttons are pressed,
        # whether it's via the keyboard or joystick
        self.keys_pressed = {}
        for button in self.buttons:
            self.keys_pressed[button] = False
        # This is a list of joystick configurations that will be populated
        # during the configuration phase
        self.joystick_config = {}
        self.quit_attempt = False

    # button is a string of the designation in the list above
    def is_pressed(self, button):
        return self.keys_pressed[button]

    # This will pump the pygame events. If this is not called every frame,
    # then the PyGame window will start to lock up.
    # This is basically a proxy method for pygame's event pump and will
    # likewise return a list of event proxies.
    def get_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.quit_attempt = True
            # This is where the keyboard events are checked
            if event.type == KEYDOWN or event.type == KEYUP:
                key_pushed_down = event.type == KEYDOWN
                button = self.key_map.get(event.key)
                if button is not None:
                    events.append(InputEvent(button, key_pushed_down))
                    self.keys_pressed[button] = key_pushed_down
        # And this is where each configured button is checked...
        for button in self.buttons:
            # determine what something like "Y" actually means in terms of the joystick
            config = self.joystick_config.get(button)
            if config is not None:
                # if the button is configured to an actual button...
                if config[0] == "is_button":
                    pushed = self.joystick.get_button(config[1])
                    if pushed != self.keys_pressed[button]:
                        events.append(InputEvent(button, pushed))
                        self.keys_pressed[button] = pushed
                # if the button is configured to a hat direction...
                elif config[0] == "is_hat":
                    status = self.joystick.get_hat(config[1])
                    if config[2] == "x":
                        amount = status[0]
                    else:
                        amount = status[1]
                    pushed = amount == config[3]
                    if pushed != self.keys_pressed[button]:
                        events.append(InputEvent(button, pushed))
                        self.keys_pressed[button] = pushed
                elif config[0] == "is_axis":
                    status = self.joystick.get_axis(config[1])
                    if config[2] == 1:
                        pushed = status > 0.5
                    else:
                        pushed = status < -0.5
                    if pushed != self.keys_pressed[button]:
                        events.append(InputEvent(button, pushed))
                        self.keys_pressed[button] = pushed
        return events

    # Any button that is currently pressed on the game pad will be toggled
    # to the button designation passed in as the 'button' parameter.
    # (as long as it isn't already in use for a different button)
    def configure_button(self, button):
        js = self.joystick
        # check buttons for activity...
        for button_index in range(js.get_numbuttons()):
            button_pushed = js.get_button(button_index)
            print(button_pushed)
            if button_pushed and not self.is_button_used(button_index):
                self.joystick_config[button] = ("is_button", button_index)
                return True
        # check hats for activity...
        # (hats are the basic direction pads)
        for hat_index in range(js.get_numhats()):
            hat_status = js.get_hat(hat_index)
            if hat_status[0] < -0.5 and not self.is_hat_used(hat_index, "x", -1):
                self.joystick_config[button] = ("is_hat", hat_index, "x", -1)
                return True
            elif hat_status[0] > 0.5 and not self.is_hat_used(hat_index, "x", 1):
                self.joystick_config[button] = ("is_hat", hat_index, "x", 1)
                return True
            if hat_status[1] < -0.5 and not self.is_hat_used(hat_index, "y", -1):
                self.joystick_config[button] = ("is_hat", hat_index, "y", -1)
                return True
            elif hat_status[1] > 0.5 and not self.is_hat_used(hat_index, "y", 1):
                self.joystick_config[button] = ("is_hat", hat_index, "y", 1)
                return True

        for axis_index in range(js.get_numaxes()):
            axis_status = js.get_axis(axis_index)
            if axis_status < -0.5 and not self.is_axis_used(axis_index, -1):
                self.joystick_config[button] = ("is_axis", axis_index, -1)
                return True
            elif axis_status > 0.5 and not self.is_axis_used(axis_index, 1):
                self.joystick_config[button] = ("is_axis", axis_index, 1)
                return True
        return False

    # The following 4 methods are helper methods used by the above method
    # to determine if a particular button/axis/hat are already
    # configured to a particular button designation
    def is_button_used(self, button_index):
        for button in self.buttons:
            config = self.joystick_config.get(button)
            if (
                config is not None
                and config[0] == "is_button"
                and config[1] == button_index
            ):
                return True
        return False

    def is_hat_used(self, hat_index, axis, direction):
        for button in self.buttons:
            config = self.joystick_config.get(button)
            if config is not None and config[0] == "is_hat":
                if (
                    config[1] == hat_index
                    and config[2] == axis
                    and config[3] == direction
                ):
                    return True
        return False

    def is_axis_used(self, axis_index, direction):
        for button in self.buttons:
            config = self.joystick_config.get(button)
            if config is not None and config[0] == "is_axis":
                if config[1] == axis_index and config[2] == direction:
                    return True
        return False

    # Set joystick information.
    # The joystick needs to be plugged in before this method is called (see main() method)
    def init_joystick(self):
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        self.joystick = joystick
        self.joystick_name = joystick.get_name()
