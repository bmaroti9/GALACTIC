import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

from star import *

SCROLL = 30


def map_mode(surface, LABEL_FONT, SCREEN_FOCUS, SPACESHIPS, SUN, scroll, PLANETS):
    global SCROLL
    surface.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        scroll = 1.08
    elif keys[pygame.K_LEFT]:
        scroll = 0.92

    x = (SUN.real_x - surface.get_width() / 2) / \
        (900 / SCROLL) + (surface.get_width() / 2)
    y = (SUN.real_y - surface.get_height() / 2) / \
        (900 / SCROLL) + (surface.get_height() / 2)

    labelled_dot(surface, [x, y], SUN.color, SUN,
                 LABEL_FONT, SUN.name, SCROLL * (SUN.size / 833), SUN.color)

    for n in PLANETS:
        x = (n.real_x - surface.get_width() / 2) / \
            (900 / SCROLL) + (surface.get_width() / 2)
        y = (n.real_y - surface.get_height() / 2) / \
            (900 / SCROLL) + (surface.get_height() / 2)

        labelled_dot(surface, [x, y], n.color, n,
                     LABEL_FONT, n.name, SCROLL * (n.size / 833), n.color)

    pygame.draw.circle(surface, (30, 150, 30), [surface.get_width() // 2, surface.get_height() // 2],  
            int(SCROLL * 0.666), 1)
    pygame.draw.circle(surface, (30, 150, 30), [surface.get_width() // 2, surface.get_height() // 2], 
            int(SCROLL * 8.333), 1)

    if SCROLL * scroll < 150 and SCROLL * scroll > 4:
        SCROLL = SCROLL * scroll

    for n in SPACESHIPS:
        x = (n.real_x - surface.get_width() / 2) / \
            (900 / SCROLL) + (surface.get_width() / 2)
        y = (n.real_y - surface.get_height() / 2) / \
            (900 / SCROLL) + (surface.get_height() / 2)
        a = distance([surface.get_width() / 2,
                     surface.get_height() / 2], [x, y])
        if a <= (SCROLL * 8.333):
            z = (250, 250, 250)
            if n == get_arrow().chosen:
                z = (250, 0, 0)
            labelled_dot(surface, (x, y), z, n, LABEL_FONT,
                         n.info["name"], 3, (200, 200, 200))


def labelled_dot(surface, pos, color, owner, LABEL_FONT, text, size, text_color):
    pygame.draw.circle(surface, color,
                       (int(pos[0]), int(pos[1])), int(size))

    hihi = LABEL_FONT.render(
        text, True, text_color)

    rect = hihi.get_rect()
    rect.center = [pos[0], pos[1] + size + 8]
    surface.blit(hihi, rect)

    mouse = pygame.mouse.get_pos()
    a = rect.topleft
    b = rect.bottomright
    c = pygame.mouse.get_pressed(3)[0]
    if a[0] < mouse[0] and mouse[0] < b[0] and a[1] < mouse[1] and mouse[1] < b[1] and c:
        get_arrow().chosen = owner


def trading_routes(surface, LABEL_FONT, PLAYER, SUN, scroll, PLANETS):

    global SCROLL
    surface.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        scroll = 1.08
    elif keys[pygame.K_LEFT]:
        scroll = 0.92

    x = (SUN.real_x - surface.get_width() / 2) / \
        (900 / SCROLL) + (surface.get_width() / 2)
    y = (SUN.real_y - surface.get_height() / 2) / \
        (900 / SCROLL) + (surface.get_height() / 2)

    labelled_dot(surface, [x, y], SUN.color, SUN, LABEL_FONT, PLAYER,
                 PLAYER, SUN.name, SCROLL * (SUN.size / 833), SUN.color)

    for n in PLANETS:
        x = (n.real_x - surface.get_width() / 2) / \
            (900 / SCROLL) + (surface.get_width() / 2)
        y = (n.real_y - surface.get_height() / 2) / \
            (900 / SCROLL) + (surface.get_height() / 2)

        labelled_dot(surface, [x, y], n.color, n,
                     LABEL_FONT, PLAYER, PLAYER, n.name, SCROLL * (n.size / 833), n.color)

    if SCROLL * scroll < 150 and SCROLL * scroll > 4:
        SCROLL = SCROLL * scroll
