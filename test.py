import os
import time
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_a, K_b, K_x, K_y, K_l, K_r, QUIT, KEYDOWN, KEYUP, K_ESCAPE


def load_png(image_name):
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
    return image, image.get_rect()


class Dorf(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.image = image
        self.rect = rect

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed


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
            if event.type == QUIT or (event.type == KEYDOWN
                                      and event.key == K_ESCAPE):
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


def main():

    fps = 30

    print(
        "Plug in a USB gamepad. Do it! Do it now! Press enter after you have done this."
    )
    wait_for_enter()

    pygame.init()

    num_joysticks = pygame.joystick.get_count()
    if num_joysticks < 1:
        print("You didn't plug in a joystick. FORSHAME!")
        return

    input_manager = InputManager()

    screen = pygame.display.set_mode((640, 480))

    button_index = 0

    dorf_image, dorf_rect = load_png("dorf.png")
    dorf = Dorf(dorf_image, dorf_rect)

    group = pygame.sprite.Group()
    group.add(dorf)

    # The main game loop
    while not input_manager.quit_attempt:
        start = time.time()

        screen.fill((0, 0, 0))
        # There will be two phases to our "game".
        is_configured = button_index >= len(input_manager.buttons)
        print(len(input_manager.buttons))
        print(button_index)
        # In the first phase, the user will be prompted to configure the joystick by pressing
        # the key that is indicated on the screen
        # You would probably do this in an input menu in your real game.
        if not is_configured:
            success = configure_phase(
                screen, input_manager.buttons[button_index], input_manager
            )
            # if the user pressed a button and configured it...
            if success:
                # move on to the next button that needs to be configured
                button_index += 1
        else:
            interaction_phase(screen, dorf, input_manager)
            # draw
            # Draw the dorf
            group.update()
            group.draw(screen)

        pygame.display.flip()
        # maintain frame rate
        difference = start - time.time()
        delay = 1.0 / fps - difference
        if delay > 0:
            time.sleep(delay)


def configure_phase(screen, button, input_manager):
    # need to pump windows events otherwise the window will lock up and die
    input_manager.get_events()
    # configure_button looks at the state of ALL buttons pressed on the joystick
    # and will map the first pressed button it sees to the current button you pass
    # in here.
    success = input_manager.configure_button(button)
    # tell user which button to configure
    write_text(screen, "Press the " + button + " button", 100, 100)
    # If a joystick button was successfully configured, return True
    return success


def interaction_phase(screen, dorf, input_manager):
    # I dunno. This doesn't do anything. But this is how
    # you would access key hit events and the like.
    # Ideal for "shooting a weapon" or "jump" sort of events
    for event in input_manager.get_events():
        if event.key == "A" and event.down:
            print("You pressed A")
        if event.key == "X" and event.up:
            input_manager.quit_attempted = True
    # ...but for things like "move in this direction", you want
    # to know if a button is pressed and held
    if input_manager.is_pressed("left"):
        dorf.move_left()
    elif input_manager.is_pressed("right"):
        dorf.move_right()
    if input_manager.is_pressed("up"):
        dorf.move_up()
    elif input_manager.is_pressed("down"):
        dorf.move_down()


# There was probably a more robust way of doing this. But
# command line interaction was not the point of the tutorial.
def wait_for_enter():
    try:
        input()
    except:
        pass


# This renders text on the game screen.
# Also not the point of this tutorial.
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


if __name__ == '__main__':
    main()
