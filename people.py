from cmath import sqrt
import math
from operator import truediv
import pygame
from pygame.locals import *
import random

from helpers import *
from sun import *
from weapons import set_marker
from star import *

class Bot(pygame.sprite.Sprite):
    def __init__(self, name, sun, planets):
        super().__init__()

        self.thrust = 0
        self.point_dir = 0
        self.unaccurate = 0
        self.name = name
        self.professional = random.randint(0, 50)
        
        self.sun = sun
        self.planets = planets
        self.avoid_object = None
        self.avoid_this = None

        self.update_timing = 5
        self.target = 0

    def controll_spacehip(self, my_spaceship, all_spaceships):
        if self.target == 0:
            self.target = random.choice(all_spaceships)
        
        if every_ticks(2):
            self.new_target(my_spaceship, all_spaceships)
        
        self.close(my_spaceship)
        
        if random.randint(0, 30) == 0:
            self.unaccurate = random.randint(-self.professional, self.professional)
            #self.unaccurate = 0
            #x = get_arrow()
            #hihi = self.planets.sprites().index(x)
            #self.target = self.planets.sprites()[x]

        
        inputs = [self.thrust, 0, 0, 0]

        angle = (self.point_dir - my_spaceship.angle) % 360

        if angle < 180:
            inputs[2] = 1
        elif angle > 180:
            inputs[1] = 1

        if random.randint(0, 30) == 1:
            inputs[3] = 1
        
        return inputs

    def new_target(self, my_spaceship, all_spaceships):
        everybody = self.get_list_of_in_range(my_spaceship, all_spaceships)

        g = gravity(my_spaceship, self.sun, self.planets)
        g_strength = distance(g, [0, 0])
        
        if len(everybody) > 0 and self.avoid_object == None:
            best = math.inf
            best_angle = 0
            for n in everybody:
                x = (my_spaceship.x_speed - n.x_speed) ** 3
                y = (my_spaceship.y_speed - n.y_speed) ** 3
                x += (my_spaceship.pos[0] - n.pos[0]) * 0.32
                y += (my_spaceship.pos[1] - n.pos[1]) * 0.32
        
        
                angle = calculate_angle([0, 0], [x, y]) + 180
                speed = math.sqrt((x ** 2) + (y ** 2))

                if speed < best:
                    # print(n)
                    best = speed
                    best_angle = angle

            self.point_dir = (best_angle + self.unaccurate) % 360

            self.update_timing = min(best // 50, 7)
            if best > 100:
                self.thrust = 1
            else:
                self.thrust = 0
        
        elif self.avoid_object != None:
            self.point_dir = (self.avoid_object + self.unaccurate) % 360
            self.thrust = 1
            self.update_timing = 2

    def random_object(self):
        #x = random.randint(0, len(self.planets))
        x = predictable_random(len(self.planets))

        if x == len(self.planets):
            hihi = self.sun
        else:
            hihi = self.planets.sprites()[x]
        
        return hihi

    def dangerous(self, my_spaceship, random_object):
        print(random_object)
        dis = distance(my_spaceship.pos, random_object.pos)
        ang = calculate_angle([0, 0], [my_spaceship.x_speed, my_spaceship.y_speed])
        aproach_pos = rotating_position(0, dis, ang, my_spaceship.pos)
        aproach_dis = distance(random_object.pos, aproach_pos)
        should = calculate_angle(random_object.pos, aproach_pos)
        spaceship_speed = distance([0, 0], [my_spaceship.x_speed, my_spaceship.y_speed])
        
        if self.avoid_object == None:
            c = (100, 250, 100)
        else:
            c = (200, 0, 0)
        set_marker(rotating_position(0, -50, should, my_spaceship.pos), c)
        
        if aproach_dis < random_object.size * 4 and (dis - random_object.size) < spaceship_speed * 900:
            return should
        return None
    
    def close(self, my_spaceship):
        
        for n in range(5):
            if self.avoid_object == None:
                self.avoid_this = self.random_object()
            
            self.avoid_object = self.dangerous(my_spaceship, self.avoid_this)

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
