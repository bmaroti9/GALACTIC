from cmath import sqrt
import math
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
        self.closest_object = sun

        self.update_timing = 10
        self.target = 0

    def controll_spacehip(self, my_spaceship, all_spaceships):
        if self.target == 0:
            self.target = random.choice(all_spaceships)

        self.recalculate_closest_object(my_spaceship)
        
        if every_ticks(self.update_timing):
            self.new_target(my_spaceship, all_spaceships)
        
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
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! [removed shooting]
            inputs[3] = 1
        
        return inputs

    def new_target(self, my_spaceship, all_spaceships):
        everybody = self.get_list_of_in_range(my_spaceship, all_spaceships)

        g = gravity(my_spaceship, self.sun, self.planets)
        g_strength = distance(g, [0, 0])
        '''
        if len(everybody) > 0:
            best = math.inf
            best_angle = 0
            for n in everybody:
                x = (my_spaceship.x_speed - n.x_speed) ** 3
                y = (my_spaceship.y_speed - n.y_speed) ** 3
                x += (my_spaceship.pos[0] - n.pos[0]) * 0.32
                y += (my_spaceship.pos[1] - n.pos[1]) * 0.32
                #x += cx
                #y += cy

                angle = calculate_angle([0, 0], [x, y]) + 180
                speed = math.sqrt((x ** 2) + (y ** 2))

                if speed < best:
                    # print(n)
                    best = speed
                    best_angle = angle

            self.point_dir = (best_angle + self.unaccurate) % 360
            if best > 100:
                self.thrust = 1
            else:
                self.thrust = 0
        elif random.randint(0, 5) <= 10:
            #x = random.randint(-100, 100) + cx
            #y = random.randint(-100, 100) + cy
            self.point_dir = calculate_angle([0, 0], [-cx, -cy]) + 180
            print("hihi", cx, cy, self.point_dir, g, [my_spaceship.x_speed, my_spaceship.y_speed])
            self.thrust = 1
        '''
        
        closest_pos = rotating_position(0, self.closest_object.size + 900, 
            calculate_angle(my_spaceship.pos, self.closest_object.pos) + 50, self.closest_object.pos) 
        
        self.target.pos

        ax = ((my_spaceship.x_speed * 1.63) + (g[0] * 180)) ** 3
        ay = ((my_spaceship.y_speed * 1.63) + (g[1] * 180)) ** 3

        bx = (my_spaceship.pos[0] - closest_pos[0]) * 0.33
        by = (my_spaceship.pos[1] - closest_pos[1]) * 0.33
        haha = math.sqrt((bx ** 2) + (by ** 2))

        if haha < 300:
            bx = (my_spaceship.pos[0] - self.target.pos[0]) * 0.33
            by = (my_spaceship.pos[1] - self.target.pos[1]) * 0.33

        he = 10

        if get_screen_focus().focus == my_spaceship:
            set_marker([ax / he, ay / he], (250, 200, 0))
            set_marker([bx / he, by / he], (0, 200, 0))
            set_marker([(ax + bx) / he, (ay + by) / he], (200, 0, 0))

        best_angle = calculate_angle([0, 0], [ax + bx, ay + by]) + 180
        best = math.sqrt(((ax + bx) ** 2) + ((ay + by) ** 2))

        self.point_dir = (best_angle + self.unaccurate) % 360
        self.update_timing = min(distance(my_spaceship.pos, self.closest_object.pos) // 200, 15)
        self.update_timing = round(max(self.update_timing, 2))

        if best > self.update_timing * 8.6:
            self.thrust = 1
        else:
            self.thrust = 0

    def close_random_object(self, my_spaceship):
        x = random.randint(0, len(self.planets))

        if x == len(self.planets):
            hihi = self.sun
        else:
            hihi = self.planets.sprites()[x]
        
        dis = distance(my_spaceship.pos, hihi.pos) - hihi.size

        ship = distance(my_spaceship.pos, self.target.pos)
        planet = distance(hihi.pos, self.target.pos)

        if ship < planet - 100:
            return [1000000000000000, hihi]

        return [dis, hihi]

    def recalculate_closest_object(self, my_spaceship):
        original = distance(my_spaceship.pos, self.closest_object.pos) - self.closest_object.size

        if random.randint(0, 5) == 0:
            ship = distance(my_spaceship.pos, self.target.pos)
            planet = distance(self.closest_object.pos, self.target.pos)

            if ship < planet - 100:
                original = 100000000

        for _ in range(3):
            x = self.close_random_object(my_spaceship)
            new = x[0]

            if new < original:
                self.closest_object = x[1]
        

    def planet_security(self):
        x = random.randint(0, len(self.planets))
        y = random.randint(0, 2)
        
        if x == len(self.planets):
            hihi = self.sun
        else:
            hihi = self.planets[x]


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
