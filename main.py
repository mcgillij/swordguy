import os
import pygame_sdl2 as pygame

def load_png(image_name):
    """ Load image and return image object """
    fullname = os.path.join('data', image_name)

    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image: ', fullname)
        raise SystemExit(message)
    return image, image.get_rect()

class Dorf(pygame.sprite.Sprite):

    speed = 10

    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = rect

    def move(self, direction):
        self.rect.move_ip(direction * self.speed, 0)


def debug_joystick():
    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()
    print(f"You have {joystick_count} joysticks connected")
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        print(f"Joystick {i}")
        # Get the name from the OS for the controller/joystick.
        joystick_name = joystick.get_name()
        print(f"Joystick name: {joystick_name}")

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        print(f"Number of axes: {axes}")

        for i in range(axes):
            axis = joystick.get_axis(i)
            print(f"Axis {i} value: {axis:>6.3f}")

        buttons = joystick.get_numbuttons()
        print(f"Number of buttons: {buttons}")

        for i in range(buttons):
            button = joystick.get_button(i)
            print(f"Button {i:>2} value: {button}")

        hats = joystick.get_numhats()
        print(f"Number of hats: {hats}")

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            print(f"Hat {i} value: {hat}")

if __name__ == "__main__":
    print("Starting")
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Sword GUY!")

    # init sprite
    dorf_image, dorf_rect = load_png("dorf.png")
    mydorf = Dorf(dorf_image, dorf_rect)

    group = pygame.sprite.Group()
    group.add(mydorf)

    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Initialize the joysticks.
    pygame.joystick.init()


    # main
    direction = 0
    while not done:
        # Events
        # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION
        for event in pygame.event.get(): # User did something.
            if event.type == pygame.QUIT: # If user clicked close.
                done = True # Flag that we are done so we exit this loop.
            elif event.type == pygame.JOYBUTTONDOWN:
                direction = 1
                print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                direction = -1
                print("Joystick button released.")
        

        mydorf.move(direction)
        # DRAW
        screen.fill(pygame.Color("white")) # pick a default fill color
        group.update()
        group.draw(screen)
        screen.blit(mydorf.image, (0,0))

        debug_joystick()

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second.
        clock.tick(60)

    pygame.quit()

