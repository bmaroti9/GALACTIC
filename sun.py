import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time
import json

from person import *

with open("names.txt", "r") as f:
    NAMES = json.load(f)

CITY2 = NAMES["city2"]

NAMES = NAMES["planets_suns"]


class Sun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.used_names = []
        self.pos = [2100, 2100]
        self.size = 2000
        self.real_x = 0
        self.real_y = 0
        self.name = NAMES[random.randint(0, len(NAMES) - 1)]
        while self.used_names.__contains__(self.name):
            self.name = NAMES[random.randint(0, len(NAMES) - 1)]
            print("blocked")
        self.used_names.append(self.name)
        print(self.name)
        self.color = (250, 170, 0)

    def update(self, surface, screen_focus, opponents):
        self.real_x = screen_focus.pos[0] - self.pos[0] + surface.get_width() / 2
        self.real_y = screen_focus.pos[1] - self.pos[1] + surface.get_height() / 2
        c = self.real_x > -self.size and self.real_x < surface.get_width() + self.size and \
            self.real_y > -self.size and self.real_y < surface.get_height() + self.size
        if c:
            
            pygame.draw.circle(surface, self.color, [
                               int(self.real_x), int(self.real_y)], self.size)

            for n in opponents:
                if distance(self.pos, n.pos) < self.size + 15 and n.dead == 0:
                    n.dead = 1
                    n.x_speed = 0
                    n.y_speed = 0


class Planet(pygame.sprite.Sprite):
    def __init__(self, SUN, PLANETS, surface):
        super().__init__()

        self.size = random.randint(100, 700)

        h = [SUN]
        for n in PLANETS:
            h.append(n)
        w = True
        while w:
            w = False
            self.pos = [random.randint(-40000, 40000),
                        random.randint(-40000, 40000)]
            for n in h:
                if distance(n.pos, self.pos) < n.size + self.size + 5000:
                    w = True
                    print("pos_block")

        self.real_x = 0
        self.real_y = 0
        self.available_reasources = planet_reasources()
        self.name = NAMES[random.randint(0, len(NAMES) - 1)]
        while SUN.used_names.__contains__(self.name):
            self.name = NAMES[random.randint(0, len(NAMES) - 1)]
            print("blocked")
        SUN.used_names.append(self.name)
        print(self.name)

        w = True
        while w:
            self.color = (random.randint(0, 250), random.randint(
                0, 250), random.randint(0, 250))
            if self.color[0] + self.color[1] + self.color[2] < 70:
                w = True
            else:
                w = False

        self.citys = []
        self.city2 = CITY2[random.randint(0, len(CITY2) - 1)]

        for _ in range(random.randint(0, round(self.size / 80))):
            self.citys.append(City(self.city2, self.available_reasources))

    def after_loading(self, surface, loaded):
        
        self.my_surface()
        
        for n in self.citys:
            n.after_loading(surface, self)

        for n in self.citys:
            self.image.blit(n.image, n.rect)
    
    def my_surface(self):
        hihi = self.size * 2 + 400
        self.image = pygame.Surface((hihi, hihi), flags=pygame.SRCALPHA)        
        pygame.draw.circle(self.image, self.color, [
                           self.image.get_width() // 2, self.image.get_height() // 2], int(self.size))
        
        self.rect = self.image.get_rect()
        self.rect.center = [20, 20]


    def update(self, surface, screen_focus, spaceships):
        self.real_x = screen_focus.pos[0] - self.pos[0] + surface.get_width() / 2
        self.real_y = screen_focus.pos[1] - self.pos[1] + surface.get_height() / 2
        c = self.real_x > -self.size and self.real_x < surface.get_width() + self.size and \
            self.real_y > -self.size and self.real_y < surface.get_height() + self.size
        if c:
            self.rect.center = [self.real_x, self.real_y]
            surface.blit(self.image, self.rect)
        
        
        for spaceship in spaceships:
            a = calculate_angle(self.pos, spaceship.pos)
            b = retrogade(spaceship.x_speed, spaceship.y_speed)
            c = (a - spaceship.angle) % 360

            if distance(self.pos, spaceship.pos) < self.size + 15 and spaceship.dead == 0:
                if spaceship.info["type"] == "lander":
                    a = calculate_angle(self.pos, spaceship.pos)
                    b = retrogade(spaceship.x_speed, spaceship.y_speed)
                    c = (a - spaceship.angle) % 360
                    l = math.sqrt((spaceship.x_speed ** 2) +
                                (spaceship.y_speed ** 2))

                    if a + 90 > b and a - 90 < b:
                        spaceship.x_speed = 0
                        spaceship.y_speed = 0
                        #n.landed = self
                    else:
                        #n.landed = False
                        pass

                    if (spaceship.dead == 0 and c < 330 and c > 30) or l > 2:
                        spaceship.dead = 1

                else:
                    spaceship.dead = 1
                    #n.landed = self
                    spaceship.x_speed = 0
                    spaceship.y_speed = 0
        

def gravity(you, sun, planets):
    dis = distance(you.pos, (sun.pos)) + 0.0001
    weight = (sun.size ** 2)
    x = ((sun.pos[0] - you.pos[0]) / (dis ** 2.5)) * weight * 0.0008
    y = ((sun.pos[1] - you.pos[1]) / (dis ** 2.5)) * weight * 0.0008

    for n in planets:
        dis = distance(you.pos, (n.pos)) + 0.0001
        weight = (n.size ** 2)
        x += ((n.pos[0] - you.pos[0]) / (dis ** 2.5)) * weight * 0.0008
        y += ((n.pos[1] - you.pos[1]) / (dis ** 2.5)) * weight * 0.0008

    return [x, y]

def calculate_trading_routes(PLANET, PLANETS):
    #finds average

    average_reasources = []

    for x in range(4):
        average_reasources.insert(0, PLANET.citys[0].reasources[x])
        for n in PLANET.citys:
            a = n.industries - n.used
            b = (average_reasources[0] + a) // 2
            average_reasources[0] = a

    average_reasources.reverse()

    #finds 

    

