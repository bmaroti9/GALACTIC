import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

from I_industries import *
from I_people import *
from map_mode import *

pygame.init()

FONT1 = pygame.font.SysFont("latinmodernmonolight", 60)
FONT2 = pygame.font.SysFont("dejavuserif", 17)
FONT3 = pygame.font.SysFont("latinmodernmonolight", 30)
FONT4 = pygame.font.SysFont("ubuntu", 26)
FONT5 = pygame.font.SysFont("latinmodernmonoslanted", 30)

CITY_TAB_NAMES = ["Industies", "Usage", "People", "Trading Map"]


class City_info(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.tab = 0
        self.people_word = ""
        self.talk_word = ""
        self.people_surf = pygame.Surface(
            (surface.get_width() - 270, surface.get_height() - 200))
        self.talk_chat = []
        self.talk_word_y = 40

        self.people_scroll = 0
        self.people_search = False
        self.talk_search = True

    def update(self, PLANET, surface, person, city, scroll, big_event, player, SUN, PLANETS):
        person.city_surf.fill((0, 0, 0))

        if city.capital == 1:
            a = 5
            blit_text(person.city_surf, "capital of planet " + PLANET.name, FONT2, (150, 150, 150),
                      (person.city_surf.get_width() / 2, 78), 1)
        else:
            a = 25

        blit_text(person.city_surf, city.name, FONT1, PLANET.color,
                  (person.city_surf.get_width() / 2, a), 1)
        pygame.draw.line(person.city_surf, PLANET.color, (100, 105),
                         (person.city_surf.get_width() - 100, 105))

        y = 140
        index = 0
        for n in CITY_TAB_NAMES:
            if index == self.tab:
                text_color = PLANET.color
                if n == "Industies":
                    Industies(person.city_surf, city,
                              city.industries, city.could_be_used, True)
                elif n == "Usage":
                    Industies(person.city_surf, city,
                              city.industries, city.used, False)
                elif n == "People":
                    People(self, person.city_surf, city,
                           PLANET, scroll, big_event)
                    #talk(person.city_surf, self, city, PLANET, big_event)
                elif n == "Trading Map":
                    trading_routes(self.people_surf, FONT2,
                                   player, SUN, 0, PLANETS)
                    person.city_surf.blit(self.people_surf, (270, 200))

            else:
                text_color = (150, 150, 150)

            x = button(person.city_surf, n, FONT3, text_color,
                       (0, 0, 0), [30, y, 0], -1, PLANET.color)
            if x:
                self.tab = index

            pygame.draw.line(person.city_surf, (150, 150, 150),
                             (0, y + 46), (230, y + 46))
            y += 50
            index += 1

            self.people_surf.fill((0, 0, 0))

        surface.blit(person.city_surf, (0, 0))
