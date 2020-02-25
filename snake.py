import pygame
from random import randint

pygame.init()

pygame.init()

screenWidth = 600
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption('Snake in Pyhton by Lukas')

clock = pygame.time.Clock()
run = True

score = 0


class cube(object):
    '''creates a new square used in the game'''

    def __init__(self, start, dirnx=1, dirny=0, color=(0, 0, 0), eyes=False):
        self.dim = [start[0], start[1], 20, 20]
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
        self.eyes = eyes

    def move(self, dirnx, dirny):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, dim)


class snake(object):
    '''creates a new snake for the player'''

    def __init__(self, pos, color=(255, 0, 0)):
        self.pos = pos
        self.color = color
        self.snake = [cube(pos, color=self.color, eyes=True)]

    def move(self):
        pass

    def addCube(self):
        pass

    def draw(self, screen):
        for part in self.snake:
            part.draw(screen)


class food(object):
    ''' creates a new food item for the snake'''

    def __init__(self, pos):
        self.hitbox = cube(pos, color=(0, 128, 0))

    def draw(self, screen):
        self.hitbox.draw(screen)
