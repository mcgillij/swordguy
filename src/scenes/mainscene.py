""" Main Scene """
import pygame
from .scene import Scene
import random

import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

from ..utils import load_image

# from bullet import Bullet
from ..dorf import Dorf

COLLISION_TYPES = {'ball': 1}
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
pymunk.pygame_util.positive_y_is_up = True


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.title = self.font.render("MainScene", True, pygame.Color("blue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = 'black'
        self.inputmanager = None
        self.next_scene = "OTHER"
        self.dorf_images = ["dorf.png", "dorf1.png", "dorf2.png"]
        self.loaded_images = [load_image(image) for image in self.dorf_images]

        print("I'm in main")
        # pymunk physics
        self.space = pymunk.Space()
        self.draw_options = pymunk.pygame_util.DrawOptions(pygame.display.get_surface())

        static_lines = [
            pymunk.Segment(self.space.static_body, (50, 50), (50, 550), 2),
            pymunk.Segment(self.space.static_body, (50, 550), (550, 550), 2),
            pymunk.Segment(self.space.static_body, (550, 550), (550, 50), 2),
            pymunk.Segment(self.space.static_body, (50, 50), (550, 50), 2),
        ]
        for line in static_lines:
            line.color = pygame.Color('lightgray')
            line.elasticity = 1.0

        self.space.add(*static_lines)

        dorf_body = pymunk.Body(500, float('inf'))
        dorf_body.position = Vec2d(0, 0)

        size = 10

        dorf_box = [(-size, -size), (-size, size), (size, size), (size, -size)]

        dorf_shape = pymunk.Poly(dorf_body, dorf_box)
        #    dorf_shape.position = Vec2d(0, 0)
        dorf_shape.collision_type = COLLISION_TYPES['ball']

        self.dorf = Dorf(self.loaded_images, dorf_body)
        # Add dorf to simulation
        self.space.add(dorf_body, dorf_shape)

        # bullet_image = load_image(
        #     "bullet.png"
        # )  # this probably needs to be only loaded once

        # setup sprite group for drawing
        self.group = pygame.sprite.Group()
        self.group.add(self.dorf)

    def get_event(self, event):
        self.interaction_phase()
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            self.persist['screen_color'] = "gold"
            self.done = True

    def draw(self, surface):
        surface.fill((0, 0, 0))
        # surface.fill(pygame.Color(self.persist['screen_color']))
        self.group.update()
        self.group.draw(surface)
        # do physics with pymunk here
        self.space.debug_draw(self.draw_options)

        surface.blit(self.title, self.title_rect)

    def update(self, dt):
        self.process_physics_bullets()
        self.space.step(dt)
        # clock.tick(fps)
        # maintain frame rate
        # difference = start - time.time()
        # delay = 1.0 / fps - difference
        # if delay > 0:
#            time.sleep(delay)

    def process_physics_bullets(self):
        if self.dorf.shooting:
            bullet_body, bullet_shape = self.shoot_a_ball((self.dorf.rect.centerx, flipy(self.dorf.rect.centery, WINDOW_HEIGHT)), random.choice([(1, 10), (-1, 10)]))
            self.space.add(bullet_body, bullet_shape)

    def interaction_phase(self):
        # actions
        for event in self.inputmanager.get_events():
            if event.key == "A" and event.down:
                print("You pressed A")
                self.dorf.shooting = True
            if event.key == "A" and event.up:
                print("You let go of A")
                self.dorf.shooting = False
            if event.key == "X" and event.up:
                self.inputmanager.quit_attempted = True
        # movement
        if self.inputmanager.is_pressed("left"):
            self.dorf.move_left()
        elif self.inputmanager.is_pressed("right"):
            self.dorf.move_right()
        if self.inputmanager.is_pressed("up"):
            self.dorf.move_up()
        elif self.inputmanager.is_pressed("down"):
            self.dorf.move_down()

    def shoot_a_ball(self, position, direction):
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
        return ball_body, ball_shape


def flipy(pymunk_y, window_height):
    """ turn pymunk_y to pygame_y """
    return int(-pymunk_y + window_height)


# def should_go_in_draw_or_update():
#            interaction_phase(dorf, input_manager)
#            # process_bullets(dorf, bullet_image, group)
#            process_physics_bullets(dorf, space)
#            # Draw phase
#            # Draw the dorf
#
#        pygame.display.flip()
#        clock.tick(fps)
#        # maintain frame rate
#        difference = start - time.time()
#        delay = 1.0 / fps - difference
#        if delay > 0:
#            time.sleep(delay)


# def process_bullets(dorf, bullet_image, group):
    # new_bullet = Bullet(bullet_image, pygame.Rect(dorf.rect.x, dorf.rect.y, 10, 10))
    # group.add(new_bullet)
