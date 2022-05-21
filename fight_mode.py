import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

from shots import *
from opponent import *
from player import *

class Screen_focus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.pos = [0, 0]
        self.x_speed = 0
        self.y_speed = 0
    
    def update(self, focus_on):
        self.pos = focus_on.pos
        self.x_speed = focus_on.x_speed
        self.y_speed = focus_on.y_speed

SCREEN_FOCUS = Screen_focus()

def get_screen_focus():
    return SCREEN_FOCUS

def fight_mode(surface, SPACESHIPS, STARS, ARROW, THRUST, SUN, fonts, FR, PLANETS, PERSON):
    surface.fill((30, 30, 45))

    for star in STARS:
        star.update(surface, [PLAYER.x_speed, PLAYER.y_speed])
    
    SUN.update(surface, PLAYER, OPPONENTS)

    for n in PLANETS:
        n.update(surface, PLAYER, OPPONENTS, PLAYER)

    for reasource in FR:
        reasource.update(PLAYER, surface)
        if random.randint(0, 3000) == 1:
            reasource.kill()
    
    #print(len(OPPONENTS))

    for spaceship in SPACESHIPS:
        spaceship.update(surface, controll_spaceship())

    speed = "{:.2f}".format(
        math.sqrt((PLAYER.x_speed ** 2) + (PLAYER.y_speed ** 2)))
    
    if float(speed) > 0.5:
        ARROW.backwards(
            retrogade(PLAYER.x_speed, PLAYER.y_speed) + 180, surface)
    ARROW.update(surface, PLAYER, fonts[0])

    SCREEN_FOCUS.update(PLAYER.apperance)

    update_shots(surface)

    hihi = fonts[0].render(
        "Speed:  " + speed, True, ((200, 0, 0)))

    song = fonts[1].render(
        "playing: CoffeeRadio - STAR KNIGHT", True, ((200, 200, 200)))

    hühü = fonts[0].render(
        "Score:  " + str(PLAYER.score), True, ((200, 200, 200)))

    hihi_rect = hihi.get_rect()
    hihi_rect.center = (surface.get_width() / 2 - 50, surface.get_height() - 20)
    song_rect = song.get_rect()
    song_rect.topright = (surface.get_width() - 20, 20)

    surface.blit(hihi, hihi_rect)
    surface.blit(song, song_rect)
    surface.blit(hühü, [20, 20])

    x = test_shots(PLAYER)
    if x and PLAYER.dead == 0:
        if not x.appointed == PLAYER and pygame.sprite.collide_mask(x, PLAYER):
            PLAYER.dead = 1
            x.kill()

    for n in OPPONENTS:
        x = test_shots(n)
        if n.c and x and n.dead == 0 and pygame.sprite.collide_mask(x, n):
            if not x.appointed == n:
                n.dead = 1
                x.kill()
            if x.appointed == PLAYER:
                PLAYER.score += 1

def land_mode(surface, STARS, PLANETS, OPPONENTS, SUN, FR, PLAYER, PERSON, scroll, big_event):  
    
    if PLAYER.mode == 0:  
        surface.fill((30, 30, 45))

        for star in STARS:
            star.update(surface, [PLAYER.x_speed, PLAYER.y_speed])

        for n in PLANETS:
            n.update(surface, PLAYER, OPPONENTS, PERSON)
        
        PLAYER.update(surface, SUN, FR, PLANETS, PERSON)

    PERSON.update(surface, PLAYER.landed, PLAYER, scroll, big_event, SUN, PLANETS)

