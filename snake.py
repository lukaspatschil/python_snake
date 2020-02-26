import pygame
from random import randint
from copy import copy

pygame.init()

pygame.init()

screenSize = 600
screen = pygame.display.set_mode((screenSize, screenSize))

pygame.display.set_caption('Snake in Pyhton by Lukas')

clock = pygame.time.Clock()
run = True

score = 0


class cube(object):
    '''creates a new square used in the game'''

    def __init__(self, start, dirnx=1, dirny=0, color=(0, 0, 0), eyes=False):
        self.dim = (start[0], start[1], 20, 20)
        self.dirn = (dirnx, dirny)
        self.color = color
        self.eyes = eyes

    def move(self):
        self.dim = (self.dim[0] + 20 * self.dirn[0],
                    self.dim[1] + 20 * self.dirn[1], 20, 20)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.dim)


class snake(object):
    '''creates a new snake for the player'''

    def __init__(self, pos, color=(255, 0, 0)):
        self.pos = pos
        self.color = color
        self.snake = [cube(pos, color=self.color, eyes=True)]

    def move(self, dirn):
        for i in range(len(self.snake) - 1, -1, -1):
            if i != 0:
                self.snake[i].dirn = copy(self.snake[i - 1].dirn)
            else:
                self.snake[i].dirn = copy(dirn)

        for part in self.snake:
            part.move()

    def add_cube(self):
        self.snake.append(cube((self.snake[-1].dim[0] - 20 * self.snake[-1].dirn[0], self.snake[-1].dim[1] -
                                20 * self.snake[-1].dirn[1]), self.snake[-1].dirn[0], self.snake[-1].dirn[1], self.color))

    def draw(self, screen):
        for part in self.snake:
            part.draw(screen)


class food(object):
    ''' creates a new food item for the snake'''

    def __init__(self, pos):
        self.hitbox = cube(pos, color=(0, 128, 0))

    def draw(self, screen):
        self.hitbox.draw(screen)


def drawGrid():
    for i in range(screenSize // 20):
        pygame.draw.line(screen, (255, 255, 255),
                         (i * 20, 0), (i * 20, screenSize))
        pygame.draw.line(screen, (255, 255, 255),
                         (0, i * 20), (screenSize, i * 20))


def redrawGameWindow():
    '''used to draw everything on the screen'''

    screen.fill((0, 0, 0))

    drawGrid()
    player.draw(screen)

    pygame.display.update()


def end_game():
    '''ends the game if the window is closed'''

    global run

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


player = snake((0, 0))
direction = (1, 0)
limiter = 0

# mainloop
while run:
    clock.tick(27)

    # makes it possible to end the game
    end_game()

    # takes the players keyboard input
    keys = pygame.key.get_pressed()

    if limiter > 5:
        limiter = 0

    # automated moving
    if limiter == 0:
        player.move(direction)

    # w -> up; s -> down; a -> left; d -> right
    if keys[pygame.K_w]:
        direction = (0, -1)
    elif keys[pygame.K_d]:
        direction = (1, 0)
    elif keys[pygame.K_s]:
        direction = (0, 1)
    elif keys[pygame.K_a]:
        direction = (-1, 0)

    if keys[pygame.K_SPACE]:
        player.add_cube()

    # increase counter to limit movespeed
    limiter += 1

    # redraw everything
    redrawGameWindow()

pygame.quit()
