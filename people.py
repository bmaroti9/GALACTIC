import math
import pygame
from pygame.locals import *
import random

from helpers import *
from sun import *

class Bot(pygame.sprite.Sprite):
    def __init__(self, name, sun, planets):
        super().__init__()

        self.thrust = 0
        self.target = 0
        self.unaccurate = 0
        self.name = name
        self.professional = random.randint(6, 60)
        self.sun = sun
        self.planets = planets
    
    def controll_spacehip(self, my_spaceship, all_spaceships):
        if random.randint(0, 12) == 1:
            self.new_target(my_spaceship, all_spaceships)
        
        if random.randint(0, 60) == 1:
            self.unaccurate = random.randint(self.professional, self.professional)
        
        inputs = [self.thrust, 0, 0, 0]

        angle = (self.target - my_spaceship.angle) % 360

        if angle < 180:
            inputs[2] = 1
        elif angle > 180:
            inputs[1] = 1

        if random.randint(0, 30) == 1:
            inputs[3] = 1
        
        return inputs

    def new_target(self, my_spaceship, all_spaceships):
        everybody = self.get_list_of_in_range(my_spaceship, all_spaceships)

        if len(everybody) > 0:
            force = gravity(my_spaceship, self.sun, self.planets)
            best = math.inf
            best_angle = 0
            for n in everybody:
                x = (my_spaceship.x_speed - n.x_speed) ** 3
                y = (my_spaceship.y_speed - n.y_speed) ** 3
                x += (my_spaceship.pos[0] - n.pos[0]) * 0.32
                y += (my_spaceship.pos[1] - n.pos[1]) * 0.32
                
                x += ((force[0] * 140) ** 18)
                y += ((force[1] * 140) ** 18)

                angle = calculate_angle([0, 0], [x, y]) + 180
                speed = math.sqrt((x ** 2) + (y ** 2))

                if speed < best:
                    # print(n)
                    best = speed
                    best_angle = angle

            self.target = (best_angle + self.unaccurate) % 360
            if best > 100:
                self.thrust = 1
            else:
                self.thrust = 0
        elif random.randint(0, 3) == 1:
            self.target = random.randint(0, 360)
            self.thrust = 1

    def get_list_of_in_range(self, my_spaceship, spaceships):
        a = []
        for n in spaceships:
            x = distance(n.pos, my_spaceship.pos)
            if x < random.randint(3500, 5000) and not n == my_spaceship:
                a.append(n)

        return a

BOTS = pygame.sprite.Group()

def add_bot(name, sun, planets):
    BOTS.add(Bot(name, sun, planets))

def dell_all_bots():
    global BOTS
    BOTS = 0
    BOTS = pygame.sprite.Group()

def get_bot_controll(my_spaceship, all_spaceships):
    names = [i.name for i in BOTS]
    index = names.index(my_spaceship.owners_name)
    a = BOTS.sprites()[index].controll_spacehip(my_spaceship, all_spaceships)

    return a