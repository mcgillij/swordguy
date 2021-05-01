""" Main game """
import sys
import pygame

from .managers import SceneManager, InputManager
from .scenes.startup import StartupScene
from .scenes.mainscene import MainScene


def main():
    """ scene manager / game loop gets called from here"""

    pygame.init()
    inputmanager = InputManager()
    screen = pygame.display.set_mode((1280, 720))
    scenes = {"STARTUP": StartupScene(),
              "MAIN": MainScene()}

    sm = SceneManager(screen, scenes, inputmanager, "STARTUP")
    sm.run()
    pygame.quit()
    sys.exit()
    # main()


if __name__ == "__main__":
    main()
