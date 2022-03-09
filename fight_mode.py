import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

from shots import *
from opponent import *

def fight_mode(surface, PLAYER, STARS, OPPONENTS, ARROW, THRUST, SUN, fonts, FR, PLANETS, PERSON):
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

    volumes = 0
    for opponent in OPPONENTS:
        x = opponent.fighting(surface, PLAYER, OPPONENTS, ARROW, FR)
        if x > volumes:
            volumes = x
        if opponent.dead > 26:
            OPPONENTS.add(Opponent(PLAYER))
            print("added")
    if volumes > 1:
        THRUST.set_volume(1)
    else:
        THRUST.set_volume(volumes)

    speed = "{:.2f}".format(
        math.sqrt((PLAYER.x_speed ** 2) + (PLAYER.y_speed ** 2)))
    
    if float(speed) > 0.5:
        ARROW.backwards(
            retrogade(PLAYER.x_speed, PLAYER.y_speed) + 180, surface)
    ARROW.update(surface, PLAYER, fonts[0])

    PLAYER.update(surface, SUN, FR, PLANETS, PERSON)

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

    PERSON.update(surface, PLAYER.landed, PLAYER, scroll, big_event)