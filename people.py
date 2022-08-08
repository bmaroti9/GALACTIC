from cmath import sqrt
import math
import pygame
from pygame.locals import *
import random

from helpers import *
from sun import *
from weapons import set_marker

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
        self.target_dis = 10
        self.planet = random.choice(self.planets.sprites()) 

    def controll_spacehip(self, my_spaceship, all_spaceships):
        if every_ticks(self.target_dis):
            self.new_target(my_spaceship, all_spaceships)
        
        if random.randint(0, 60) == 1:
            #self.unaccurate = random.randint(-self.professional, self.professional)
            self.unaccurate = 0
        
        inputs = [self.thrust, 0, 0, 0]

        angle = (self.target - my_spaceship.angle) % 360

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
        cx = (my_spaceship.x_speed * (g[0] * 200)) ** 7
        cy = (my_spaceship.y_speed * (g[1] * 200)) ** 7
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

            self.target = (best_angle + self.unaccurate) % 360
            if best > 100:
                self.thrust = 1
            else:
                self.thrust = 0
        elif random.randint(0, 5) <= 10:
            #x = random.randint(-100, 100) + cx
            #y = random.randint(-100, 100) + cy
            self.target = calculate_angle([0, 0], [-cx, -cy]) + 180
            print("hihi", cx, cy, self.target, g, [my_spaceship.x_speed, my_spaceship.y_speed])
            self.thrust = 1
        '''

        closest_pos = rotating_position(0, self.planet.size - 10, 
                    calculate_angle(my_spaceship.pos, self.planet.pos), self.planet.pos) 

        ax = ((my_spaceship.x_speed * 1.7) + (g[0] * 140)) ** 3
        ay = ((my_spaceship.y_speed * 1.7) + (g[1] * 140)) ** 3
        
        bx = (my_spaceship.pos[0] - closest_pos[0]) * 0.33
        by = (my_spaceship.pos[1] - closest_pos[1]) * 0.33
        
        he = 10

        if get_screen_focus().focus == my_spaceship:
            set_marker([ax / he, ay / he], (250, 200, 0))
            set_marker([bx / he, by / he], (0, 200, 0))
            set_marker([(ax + bx) / he, (ay + by) / he], (200, 0, 0))

        best_angle = calculate_angle([0, 0], [ax + bx, ay + by]) + 180
        best = math.sqrt(((ax + bx) ** 2) + ((ay + by) ** 2))

        self.target = (best_angle + self.unaccurate) % 360
        self.target_dis = min(max(distance(my_spaceship.pos, self.planet.pos) // 200, 2), 80)
        
        if best > self.target_dis * 8.6:
            self.thrust = 1
        else:
            self.thrust = 0

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