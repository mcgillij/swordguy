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
# pymunk.pygame_util.positive_y_is_up = True


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
        dorf_shape.collision_type = COLLISION_TYPES['ball']

        self.dorf = Dorf(self.loaded_images, dorf_body)
        # Add dorf to simulation
        self.space.add(dorf_body, dorf_shape)

        # setup sprite group for drawing
        self.group = pygame.sprite.Group()
        self.group.add(self.dorf)

    def get_event(self, event):
        # Translate pygame events into our events
        for event in self.inputmanager.process_event(event):
            if event.key == "A" and event.down:
                print("You pressed A")
                self.dorf.shooting = True
            if event.key == "A" and event.up:
                print("You let go of A")
                self.dorf.shooting = False
            if event.key == "X" and event.up:
                # quit
                self.done = True
        # movement
        if self.inputmanager.is_pressed("left"):
            self.dorf.move_left()
        elif self.inputmanager.is_pressed("right"):
            self.dorf.move_right()
        if self.inputmanager.is_pressed("up"):
            self.dorf.move_up()
        elif self.inputmanager.is_pressed("down"):
            self.dorf.move_down()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        # surface.fill(pygame.Color(self.persist['screen_color']))
        self.group.draw(surface)
        # draw pymunk here
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(surface))

        surface.blit(self.title, self.title_rect)

    def update(self, dt):
        self.group.update()
        self.process_physics_bullets()
        physics_tick = dt / 1000.0
        self.space.step(physics_tick)

    def process_physics_bullets(self):
        if self.dorf.shooting:
            position = (self.dorf.rect.centerx, self.dorf.rect.centery)
            direction = random.choice([(1, 10), (-1, 10)])
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
            self.space.add(ball_body, ball_shape)


def flipy(pymunk_y, window_height):
    """ turn pymunk_y to pygame_y """
    return int(-pymunk_y + window_height)
