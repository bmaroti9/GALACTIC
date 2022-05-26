import pygame

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


class Joystick(object):
    def __init__(self):
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def get_axes(self):
        axes = self.joystick.get_numaxes()
        a = []

        for i in range(axes):
            axis = self.joystick.get_axis(i)
            a.append(axis)

        return a
    
    def get_button(self):
        a = []
        buttons = self.joystick.get_numbuttons()

        for i in range(buttons):
            button = self.joystick.get_button(i)
            a.append(button)

        return a

def get_axis():
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    a = []
    axes = joystick.get_numaxes()
    for i in range(axes):
        axis = joystick.get_axis(i)
        a.append(axis)

    return a


def test2(clock):
    done = False
    step = 0
    # clock = pygame.time.Clock()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while not done:
        for event in pygame.event.get():  # User did something.
            if event.type == pygame.QUIT:  # If user clicked close.
                done = True  # Flag that we are done so we exit this loop.
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

        a = []
        axes = joystick.get_numaxes()

        for i in range(axes):
            axis = joystick.get_axis(i)
            a.append(axis)

        print(step, a)
        step += 1

        pygame.display.update()
        clock.tick(30)

    sys.exit()

def test():
    pygame.init()

    # Set the width and height of the screen (width, height).
    screen = pygame.display.set_mode((500, 700))

    pygame.display.set_caption("My Game")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Initialize the joysticks.
    # pygame.joystick.init()

    # Get ready to print.
    textPrint = TextPrint()

    # -------- Main Program Loop -----------
    while not done:
        #
        # EVENT PROCESSING STEP
        #
        # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION
        for event in pygame.event.get():  # User did something.
            if event.type == pygame.QUIT:  # If user clicked close.
                done = True  # Flag that we are done so we exit this loop.
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

        #
        # DRAWING STEP
        #
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        textPrint.reset()

        # Get count of joysticks.
        #joystick_count = pygame.joystick.get_count()

        #textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
        # textPrint.indent()

        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        a = []
        axes = joystick.get_numaxes()

        for i in range(axes):
            axis = joystick.get_axis(i)
            a.append(axis)

        print(a)

        #
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        #

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second.
        clock.tick(20)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()


if __name__ == '__main__':
    test()
