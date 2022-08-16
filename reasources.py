import imp
import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

from helpers import *

FR = pygame.sprite.Group()

class floating_resource(pygame.sprite.Sprite):
    def __init__(self, color, amount, pos, reasource, speed):
        super().__init__()

        self.color = color
        self.pos = [pos[0], pos[1]]
        self.amount = amount
        self.speed = [speed[0] + random.randint(-2, 2), speed[1] + random.randint(-2, 2)]
        self.reasource = reasource
        self.c = False

    def update(self, screen_focus, surface):
        self.pos[0] += (self.speed[0] * 0.7)
        self.pos[1] += (self.speed[1] * 0.7)
        
        self.real_x = screen_focus.pos[0] - self.pos[0] + surface.get_width() / 2
        self.real_y = screen_focus.pos[1] - self.pos[1] + surface.get_height() / 2

        self.c = self.real_x > -100 and self.real_x < surface.get_width() + 100 and \
            self.real_y > -100 and self.real_y < surface.get_height() + 100

        if self.c:
            pygame.draw.circle(surface, self.color, (int(self.real_x), 
                        int(self.real_y)), self.amount // 10)

def add_reasource(color, amount, pos, reasource, speed):
    global FR
    FR.add(floating_resource(color, amount, pos, reasource, speed))

def update_reasources(surface):
    global FR
    for reasource in FR:
        reasource.update(get_screen_focus(), surface)
        if random.randint(0, 3000) == 1:
            reasource.kill()

def kill_all_reasources():
    FR = 0
    FR = pygame.sprite.Group()

def check_reasources(pos, FR):
    for n in FR:
        if n.c:
            x = distance(pos, [n.real_x, n.real_y])
            if x < (n.amount / 10) + 50:
                return n
    
    return 0

POINTS = []

def add_point(pos):
    global POINTS
    POINTS.append(pos)

def thrust_animation(surface):
    global POINTS
    for n in range(len(POINTS) - 1):
        a = get_screen_pos(POINTS[n], surface)
        b = get_screen_pos(POINTS[n + 1], surface)        
        pygame.draw.line(surface, (50, 50, 200), a, b, 15 - n)

def manage_points():
    global POINTS

    if len(POINTS) > 6:
        del POINTS[0]

def draw_thrust(surface):
    global POINTS
    manage_points()
    print("hihi ", POINTS)
    thrust_animation(surface)
    print("haha", POINTS)
