import pygame
from random import randint
from copy import copy

pygame.init()

pygame.init()

screenSize = 600
screen = pygame.display.set_mode((screenSize, screenSize))

pygame.display.set_caption('Snake in Pyhton by lukas')

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
        self.dim = (in_bounds(self.dim[0] + 20 * self.dirn[0]),
                    in_bounds(self.dim[1] + 20 * self.dirn[1]), 20, 20)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.dim)

        if self.eyes:
            pygame.draw.circle(screen, (0, 0, 0),
                               (self.dim[0] + 10 - abs(self.dirn[1]) * 5, self.dim[1] + 10 - abs(self.dirn[0]) * 5), 3)
            pygame.draw.circle(screen, (0, 0, 0),
                               (self.dim[0] + 10 + abs(self.dirn[1]) * 5, self.dim[1] + 10 + abs(self.dirn[0]) * 5), 3)


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

    def hit(self):
        print('hit!')


def drawGrid():
    '''draws a white grid of the board'''
    for i in range(screenSize // 20):
        pygame.draw.line(screen, (255, 255, 255),
                         (i * 20, 0), (i * 20, screenSize))
        pygame.draw.line(screen, (255, 255, 255),
                         (0, i * 20), (screenSize, i * 20))


def redrawGameWindow():
    '''used to draw everything on the screen'''

    screen.fill((0, 0, 0))

    # if you want a white grid
    # drawGrid()

    for item in reversed(objects):
        item.draw(screen)

    pygame.display.update()


def end_game():
    '''ends the game if the window is closed'''

    global run

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


def lose_game():
    '''if the player loses this should be executed'''

    global run

    run = False

    fontHit = pygame.font.SysFont('comicsans', 40)
    text = fontHit.render('You lost! Your score is: ' +
                          str(score), 1, (255, 218, 94))
    screen.blit(text, (screenSize // 2 - (text.get_width() // 2), 200))
    pygame.display.update()

    i = 0
    while i < 300:
        pygame.time.delay(10)
        i += 1


def in_bounds(x):
    '''calculates if the next coordinate is on the screen or not'''
    if x >= 600:
        return 0
    elif x < 0:
        return 600
    else:
        return x


objects = [snake((0, 0))]

direction = (1, 0)
limiter = 1
food_spawn = 1

# mainloop
if __name__ == "__main__":
    while run:
        clock.tick(27)

        # makes it possible to end the game
        end_game()

        # takes the players keyboard input
        keys = pygame.key.get_pressed()

        # set the intervall the snake movess
        if limiter > 5:
            limiter = 0

        # food spawn timer reset
        if food_spawn > 1000:
            food_spawn = 0

        # automated moving
        if limiter == 0:
            objects[0].move(direction)

        # spawning of food
        if len(objects) == 1 or food_spawn == 0:
            rand_spawn = (randint(0, (screenSize - 20) / 20) * 20,
                          randint(0, (screenSize - 20) / 20) * 20)
            objects.append(food(rand_spawn))

        # check if food gets eaten
        for item in objects:
            if item is not objects[0]:
                if objects[0].snake[0].dim[1] < item.hitbox.dim[1] + item.hitbox.dim[3] and objects[0].snake[0].dim[1] + objects[0].snake[0].dim[3] > item.hitbox.dim[1]:
                    if objects[0].snake[0].dim[0] + objects[0].snake[0].dim[2] > item.hitbox.dim[0] and objects[0].snake[0].dim[0] < item.hitbox.dim[0] + item.hitbox.dim[2]:
                        objects.remove(item)
                        objects[0].add_cube()
                        score += 1

        for part in objects[0].snake:
            if part is not objects[0].snake[0]:
                if objects[0].snake[0].dim[1] < part.dim[1] + part.dim[3] and objects[0].snake[0].dim[1] + objects[0].snake[0].dim[3] > part.dim[1]:
                    if objects[0].snake[0].dim[0] + objects[0].snake[0].dim[2] > part.dim[0] and objects[0].snake[0].dim[0] < part.dim[0] + part.dim[2]:
                        lose_game()

        # w -> up; s -> down; a -> left; d -> right
        if keys[pygame.K_w] and direction != (0, 1):
            direction = (0, -1)
            limiter = -1
        elif keys[pygame.K_d] and direction != (-1, 0):
            direction = (1, 0)
            limiter = -1
        elif keys[pygame.K_s] and direction != (0, -1):
            direction = (0, 1)
            limiter = -1
        elif keys[pygame.K_a] and direction != (1, 0):
            direction = (-1, 0)
            limiter = -1

        # only for testing
        # if keys[pygame.K_SPACE]:
        #    objects[0].add_cube()

        # increase counter to limit movespeed
        limiter += 1

        # food spawn timer
        food_spawn += 1

        # redraw everything
        redrawGameWindow()

    pygame.quit()
