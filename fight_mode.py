import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

from weapons import *
from network_helper import *
from opponent import *
from player import *
from star import *
from sun import *
from reasources import *

def fight_mode(surface, STARS, THRUST, SUN, fonts, PLANETS, PERSON):
    SPACESHIPS = get_spaceships()
    #print("L", SPACESHIPS)
    surface.fill((30, 30, 45))

    for star in STARS:
        star.update(surface, [SCREEN_FOCUS.x_speed, SCREEN_FOCUS.y_speed])
    
    SUN.update(surface, SCREEN_FOCUS, SPACESHIPS)

    for n in PLANETS:
        n.update(surface, SCREEN_FOCUS, SPACESHIPS)
    
    draw_thrust(surface)

    for spaceship in SPACESHIPS:
        a = gravity(spaceship, SUN, PLANETS)
        spaceship.x_speed += a[0]
        spaceship.y_speed += a[1]
        spaceship.update(surface)

    update_reasources(surface)
    blit_marker(surface)
    
    speed = "{:.2f}".format(
        math.sqrt((SCREEN_FOCUS.x_speed ** 2) + (SCREEN_FOCUS.y_speed ** 2)))
    
    if float(speed) > 0.5:
        backwards_arrow(
            retrogade(SCREEN_FOCUS.x_speed, SCREEN_FOCUS.y_speed) + 180, surface)
    guide_arrow(surface, SCREEN_FOCUS, fonts[0])

    update_screen_focus(SPACESHIPS)

    update_shots(surface)
    update_bombs(surface, SPACESHIPS)

    hihi = fonts[0].render(
        "Speed:  " + speed, True, ((200, 0, 0)))

    song = fonts[1].render(
        "playing: CoffeeRadio - STAR KNIGHT", True, ((200, 200, 200)))

    hühü = fonts[0].render(
        "Score:  " + str(get_screen_focus().score), True, ((200, 200, 200)))

    hihi_rect = hihi.get_rect()
    hihi_rect.center = (surface.get_width() / 2 - 50, surface.get_height() - 20)
    song_rect = song.get_rect()
    song_rect.topright = (surface.get_width() - 20, 20)

    surface.blit(hihi, hihi_rect)
    surface.blit(song, song_rect)
    surface.blit(hühü, [20, 20])

    for n in SPACESHIPS:
        x = test_shots(n)
        if n.c and x and n.dead == 0 and pygame.sprite.collide_mask(x, n):
            if not x.appointed == n:
                n.dead = 1
                x.kill()
                if get_screen_focus().focus == n:
                    set_focus(x.appointed)
                x.appointed.score += 1

def land_mode(surface, STARS, PLANETS, OPPONENTS, SUN, FR, PLAYER, PERSON, scroll, big_event):  
    
    if PLAYER.mode == 0:  
        surface.fill((30, 30, 45))

        for star in STARS:
            star.update(surface, [PLAYER.x_speed, PLAYER.y_speed])

        for n in PLANETS:
            n.update(surface, PLAYER, OPPONENTS, PERSON)
        
        PLAYER.update(surface, SUN, FR, PLANETS, PERSON)

    PERSON.update(surface, PLAYER.landed, PLAYER, scroll, big_event, SUN, PLANETS)
