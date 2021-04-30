""" Test for a bit of a joystick framework """
import time
import random

import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

from utils import load_image

# from bullet import Bullet
from dorf import Dorf
from inputmanager import InputManager

COLLISION_TYPES = {'ball': 1}

WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 768


def flipy(pymunk_y, window_height):
    """ turn pymunk_y to pygame_y """
    return int(-pymunk_y + window_height)


def shoot_a_ball(space, position, direction):
    ball_body = pymunk.Body(1, float("inf"))
    ball_body.position = position

    ball_shape = pymunk.Circle(ball_body, 5)
    ball_shape.color = pygame.Color('Green')
    ball_shape.elasticity = 1.0
    ball_shape.collision_type = COLLISION_TYPES['ball']

    ball_body.apply_impulse_at_local_point(Vec2d(*direction))

    def constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * 400

    ball_body.velocity_func = constant_velocity
    space.add(ball_body, ball_shape)


def main():
    """ Main game loop """

    fps = 60
    dt = 1.0 / fps

    print("Plug in a USB gamepad! Press <ENTER> after you have done this.")

    wait_for_enter()

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # pymunk physics
    space = pymunk.Space()
    pymunk.pygame_util.positive_y_is_up = True
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    static_lines = [
        pymunk.Segment(space.static_body, (50, 50), (50, 550), 2),
        pymunk.Segment(space.static_body, (50, 550), (550, 550), 2),
        pymunk.Segment(space.static_body, (550, 550), (550, 50), 2),
        pymunk.Segment(space.static_body, (50, 50), (550, 50), 2),
    ]
    for line in static_lines:
        line.color = pygame.Color('lightgray')
        line.elasticity = 1.0

    space.add(*static_lines)

    num_joysticks = pygame.joystick.get_count()
    if num_joysticks < 1:
        print("You didn't plug in a joystick. FORSHAME!")
        return

    # Probably need some kinda state manager

    input_manager = InputManager()

    button_index = 0

    dorf_images = ["dorf.png", "dorf1.png", "dorf2.png"]
    loaded_images = [load_image(image) for image in dorf_images]

    dorf_body = pymunk.Body(500, float('inf'))
    dorf_body.position = Vec2d(0, 0)

    size = 10

    dorf_box = [(-size, -size), (-size, size), (size, size), (size, -size)]

    dorf_shape = pymunk.Poly(dorf_body, dorf_box)
#    dorf_shape.position = Vec2d(0, 0)
    dorf_shape.collision_type = COLLISION_TYPES['ball']

    dorf = Dorf(loaded_images, dorf_body)
    # Add dorf to simulation
    space.add(dorf_body, dorf_shape)

    # bullet_image = load_image(
    #     "bullet.png"
    # )  # this probably needs to be only loaded once

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
            # process_bullets(dorf, bullet_image, group)
            process_physics_bullets(dorf, space)
            # Draw phase
            # Draw the dorf
            group.update()
            group.draw(screen)
            # do physics with pymunk here
            space.debug_draw(draw_options)
            space.step(dt)

        pygame.display.flip()
        clock.tick(fps)
        # maintain frame rate
        difference = start - time.time()
        delay = 1.0 / fps - difference
        if delay > 0:
            time.sleep(delay)


def process_physics_bullets(dorf, space):
    if dorf.shooting:
        shoot_a_ball(space, (dorf.rect.centerx, flipy(dorf.rect.centery, WINDOW_HEIGHT)), random.choice([(1, 10), (-1, 10)]))
# def process_bullets(dorf, bullet_image, group):
        # new_bullet = Bullet(bullet_image, pygame.Rect(dorf.rect.x, dorf.rect.y, 10, 10))
        # group.add(new_bullet)


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
    import sys
    from scenemanager import SceneManager
    from scenes import StartupScene, MainScene, OtherScene

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    scenes = {"STARTUP": StartupScene(),
              "MAIN": MainScene(),
              "OTHER": OtherScene()}

    sm = SceneManager(screen, scenes, "STARTUP")
    sm.run()
    pygame.quit()
    sys.exit()
    # main()
