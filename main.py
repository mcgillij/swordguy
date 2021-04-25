""" Test for a bit of a joystick framework """
import time

import pygame

from utils import load_image

from bullet import Bullet
from dorf import Dorf
from inputmanager import InputManager


def main():
    """ Main game loop """

    fps = 30

    print("Plug in a USB gamepad! Press <ENTER> after you have done this.")

    wait_for_enter()

    pygame.init()

    num_joysticks = pygame.joystick.get_count()
    if num_joysticks < 1:
        print("You didn't plug in a joystick. FORSHAME!")
        return

    # Probably need some kinda state manager

    input_manager = InputManager()

    screen = pygame.display.set_mode((1024, 768))

    button_index = 0

    dorf_images = ["dorf.png", "dorf1.png", "dorf2.png"]
    loaded_images = [load_image(image) for image in dorf_images]

    dorf = Dorf(loaded_images, loaded_images[0].get_rect())
    bullet_image = load_image(
        "bullet.png"
    )  # this probably needs to be only loaded once

    # setup sprite group for drawing
    group = pygame.sprite.Group()
    group.add(dorf)

    # The main game loop
    while not input_manager.quit_attempt:
        start = time.time()

        screen.fill((0, 0, 0))
        # There will be two phases to our "game".
        is_configured = button_index >= len(input_manager.buttons)
        # In the first phase, the user will be prompted to configure the joystick by pressing
        if not is_configured:
            success = configure_phase(
                screen, input_manager.buttons[button_index], input_manager
            )
            # if the user pressed a button and configured it...
            if success:
                # move on to the next button that needs to be configured
                button_index += 1
        else:
            interaction_phase(dorf, input_manager)
            process_bullets(dorf, bullet_image, group)
            # Draw phase
            # Draw the dorf
            group.update()
            group.draw(screen)

        pygame.display.flip()
        # maintain frame rate
        difference = start - time.time()
        delay = 1.0 / fps - difference
        if delay > 0:
            time.sleep(delay)


def process_bullets(dorf, bullet_image, group):
    if dorf.shooting:
        new_bullet = Bullet(bullet_image, pygame.Rect(dorf.rect.x, dorf.rect.y, 10, 10))
        group.add(new_bullet)


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


def interaction_phase(dorf, input_manager):
    # actions
    for event in input_manager.get_events():
        if event.key == "A" and event.down:
            print("You pressed A")
            dorf.shooting = True
        if event.key == "A" and event.up:
            print("You let go of A")
            dorf.shooting = False
        if event.key == "X" and event.up:
            input_manager.quit_attempted = True
    # movement
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


if __name__ == "__main__":
    main()
