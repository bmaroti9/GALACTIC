import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time
import json

from City_info import *

pygame.init()

with open("ships.txt", "r") as f:
    TALKING = json.load(f)


class Person(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.images = []
        for n in [1, 2, 3, 4]:
            image = pygame.image.load(
                "images/tukiemberke" + str(n) + ".png").convert_alpha(surface)
            image = pygame.transform.rotozoom(
                image, 0.0, 0.1)
            self.images.append(image)

        self.timer = 0
        self.current_image = 0
        self.pos = [0, 0]
        self.city_surf = pygame.Surface(
            (surface.get_width(), surface.get_height()))
        self.info_view = 0
        self.height = 0

        global CITY_INFO
        CITY_INFO = City_info(surface)

    def update(self, surface, PLANET, PLAYER, scroll, big_event, SUN, PLANETS):
        direction = calculate_angle(PLANET.pos, self.pos)

        if self.timer > 0:
            self.timer -= 1

        keys = pygame.key.get_pressed()
        flip = False
        
        if pygame.key.get_mods() == 512 and self.timer < 1:
            self.timer = 20
            if self.info_view == 0:
                pos_to_planet = [PLANET.pos[0] - self.pos[0] +
                                 PLANET.image.get_width() / 2, PLANET.pos[1] - self.pos[1] +
                                 PLANET.image.get_height() / 2]
                for n in PLANET.citys:
                    a = distance(pos_to_planet, n.pos_to_planet)
                    if a < n.image.get_width() * 0.6:
                        self.info_view = n
            else:
                self.info_view = 0
        if keys[pygame.K_RIGHT]:
            self.current_image += 0.1
            self.pos = rotating_position(
                0, self.height, direction + (180 - 110 / PLANET.size), PLANET.pos)
        elif keys[pygame.K_LEFT]:
            self.current_image += 0.1
            flip = True
            self.pos = rotating_position(
                0, self.height, direction + (180 + 110 / PLANET.size), PLANET.pos)
        else:
            self.current_image = 0

        state = round(((self.current_image) % 4) + 0.5)

        image = self.images[STEPS[state]]
        image = pygame.transform.flip(image, flip, False)
        image = pygame.transform.rotate(image, direction)
        rect = image.get_rect()
        rect.center = rotating_position(
            0, 10, direction, [surface.get_width() / 2, surface.get_height() / 2])
        surface.blit(image, rect)

        if PLAYER.mode != 1:
            if self.info_view == 0:
                PLAYER.mode = 0
            else:
                PLAYER.mode = 0.1
                CITY_INFO.update(PLANET, surface, self,
                                 self.info_view, scroll, big_event, PLAYER, SUN, PLANETS)


class City(pygame.sprite.Sprite):
    def __init__(self, city2, available_reasources):
        super().__init__()

        self.name = CITY1[random.randint(0, len(CITY1) - 1)] + city2
        self.city_type = random.randint(1, 4)
        self.angle = random.randint(1, 360)
        self.pos_to_planet = [- 5000, - 5000]
        self.could_be_used = city_reasources(available_reasources)
        self.industries = used_reasources(self.could_be_used)
        self.used = USED_for_citys(self.industries)
        self.capital = random.randint(0, 1)
        self.people = []
        for _ in range(random.randint(10, 100)):
            self.people.append(random_name())

    def after_loading(self, surface, planet):
        forever = 1

        while not forever == 9:
            if forever == 0:
                self.angle = random.randint(1, 360)

            self.pos_to_planet = rotating_position(
                0, planet.size + CITY_BONUS_SIZE[self.city_type - 1], self.angle, [
                    planet.image.get_width() / 2, planet.image.get_height() / 2])

            forever = 9
            for n in planet.citys:
                a = abs(n.pos_to_planet[0] - self.pos_to_planet[0]) + \
                    abs(n.pos_to_planet[1] - self.pos_to_planet[1])
                if a < 300 and not n == self:
                    forever = 0

        self.image = pygame.image.load(
            "images/varos" + str(self.city_type) + ".png").convert_alpha(surface)
        self.image = pygame.transform.rotozoom(
            self.image, self.angle, CITY_SIZE[self.city_type - 1])
        self.rect = self.image.get_rect()
        self.rect.center = self.pos_to_planet


STEPS = [0, 1, 2, 3, 2]

CITY_BONUS_SIZE = [10, 10, 30, 80]
CITY_SIZE = [0.08, 0.14, 0.17, 0.2]

with open("names.txt", "r") as f:
    NAMES = json.load(f)

CITY1 = NAMES["city1"]

CITY_INFO = 0
