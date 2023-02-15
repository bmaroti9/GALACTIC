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
        self.get_rid = 10

    def controll_spacehip(self, my_spaceship, all_spaceships):
        if random.randint(0, 2) == 0:
            self.close(my_spaceship, all_spaceships)
        
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

        g = gravity(my_spaceship.pos, self.sun, self.planets)
        g_strength = distance(g, [0, 0])
        
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
    
    def close(self, my_spaceship, all_spaceships):
        if self.get_rid > 0:
            self.get_rid -= 1
            return 0

        interfere = False
        hihi = [self.sun]
        for n in self.planets:
            hihi.append(n)
        
        v = distance([0, 0], [my_spaceship.x_speed, my_spaceship.y_speed])
        if v != 0:
            for n in hihi:
                s = distance(my_spaceship.pos, n.pos)
                t = s / v
                tpos = [my_spaceship.pos[0] + my_spaceship.x_speed * t, 
                        my_spaceship.pos[1] + my_spaceship.y_speed * t]
                if distance(tpos, n.pos) < n.size * 3 or s < n.size + 500:
                    last_a = v / t
                    if last_a > my_spaceship.info["engine_efficiancy"] * 0.9 - 0.03 or s < n.size + 500:
                        self.point_dir = calculate_angle(n.pos, my_spaceship.pos)
                        set_marker(rotating_position(0, -100, self.point_dir, my_spaceship.pos), 
                                (250, 250, 0))
                        self.thrust = 1
                        interfere = True
                        self.get_rid = 5
        
        if not interfere:
            self.new_target(my_spaceship, all_spaceships)


    def get_list_of_in_range(self, my_spaceship, spaceships):
        a = []
        for n in spaceships:
            x = distance(n.pos, my_spaceship.pos)
            if x < random.randint(40000, 40000) and not n == my_spaceship:
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
