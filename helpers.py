import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time
import json
import os

print(os.listdir())

with open("names_first.txt", "r") as f:
    a = json.load(f)
    BOY = a[0]
    GIRL = a[1]

with open("names_last.txt", "r") as f:
    LAST_NAMES = json.load(f)

VOLUME = 0

def add_volume(amount):
    global VOLUME
    if amount >= 1:
        VOLUME += amount

def get_volume():
    global VOLUME
    a = VOLUME
    VOLUME = 0
    return int(a)

class Screen_focus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.focus = 0
        self.pos = [0, 0]
        self.mode = 1
        self.x_speed = 0
        self.y_speed = 0
        self.name_of_focus = 0
        self.score = 0
    
    def update(self, spaceships):
        self.score = self.focus.score
        self.pos = self.focus.pos
        self.x_speed = self.focus.x_speed
        self.y_speed = self.focus.y_speed
        if self.focus.dead == "Changed":
            self.x_speed = 0
            self.y_speed = 0
            try:    
                self.focus = random.choice(spaceships)
            except:
                pass
        

SCREEN_FOCUS = Screen_focus()

def get_distance_from_focus(pos):
    a = distance(SCREEN_FOCUS.pos, pos)
    return a

def set_focus(on):
    SCREEN_FOCUS.focus = on

def update_screen_focus(spaceships):
    SCREEN_FOCUS.update(spaceships)

def get_screen_focus():
    return SCREEN_FOCUS

def get_view_mode():
    return SCREEN_FOCUS.mode

def reverse_view_mode():
    global SCREEN_FOCUS
    SCREEN_FOCUS.mode = -SCREEN_FOCUS.mode

def rotating_position(x, y, direction, pos):
    a = pos[0] + (x * math.cos(-direction / 180.0 *
                               math.pi) + y * math.sin(-direction / 180.0 * math.pi))
    b = pos[1] + \
        (-y * math.cos(-direction / 180.0 * math.pi) +
         x * math.sin(-direction / 180.0 * math.pi))

    return [a, b]


def calculate_angle(pos1, pos2):
    x = pos1[0] - pos2[0]
    y = pos1[1] - pos2[1]
    return 0 - (math.atan2(y, x) / math.pi * 180) - 90


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def retrogade(x, y):
    x = 0 - (math.atan2(y, x) / math.pi * 180) - 90
    return x

def rev_percent(num, out_of):
    return (out_of - num) / out_of


def real_angle(target, position):
    if isinstance(target, pygame.sprite.Sprite):
        angle = calculate_angle(
            position, target.pos) + random.randint(-70, 70)
    elif isinstance(target, list):
        angle = calculate_angle(
            position, target) + random.randint(-70, 70)
    else:
        angle = target

    return angle


def intpos(pos):
    return (int(pos[0]), int(pos[1]))


def button(surface, text, font, text_color, rect_color, pos, width, tuch_color, bonus_pos=[0, 0]):
    hihi = font.render(
        text, True, text_color)
    rect = hihi.get_rect()
    if pos[2] == 0:
        rect.topleft = [pos[0], pos[1]]
    else:
        rect.midtop = [pos[0], pos[1]]

    rect = pygame.Rect((rect.left - 5, rect.top + 10),
                       (hihi.get_width() + 10, hihi.get_height() - 20))
    #pygame.Rect(left, top, width, height)

    mouse = pygame.mouse.get_pos()
    mouse = [mouse[0] - bonus_pos[0], mouse[1] - bonus_pos[1]]
    a = rect.topleft
    b = rect.bottomright
    c = pygame.mouse.get_pressed(3)[0]
    if a[0] < mouse[0] and mouse[0] < b[0] and a[1] < mouse[1] and mouse[1] < b[1]:
        hihi = font.render(
            text, True, tuch_color)

    pygame.draw.rect(surface, rect_color, rect, width)
    rect.topleft = [rect.topleft[0] + 5, rect.topleft[1] - 10]
    surface.blit(hihi, rect)

    if a[0] < mouse[0] and mouse[0] < b[0] and a[1] < mouse[1] and mouse[1] < b[1] and c:
        return True

    return False


def blit_text(surface, text, font, color, pos, center):
    hihi = font.render(
        text, True, color)
    rect = hihi.get_rect()
    if center == 0:
        rect.topleft = [pos[0], pos[1]]
    elif center == 1:
        rect.midtop = [pos[0], pos[1]]
    elif center == 2:
        rect.midleft = [pos[0], pos[1]]
    elif center == 3:
        rect.topright = [pos[0], pos[1]]
    surface.blit(hihi, rect)


def planet_reasources():
    a = []
    for n in range(4):
        a.append(random.randint(-20, 20))

    return a


def city_reasources(planets_reasources):
    a = planet_reasources()
    b = []
    for n in range(4):
        x = a[n] * planets_reasources[n]
        if x > 0:
            b.append(round(x * 0.3))
        else:
            b.append(0)

    return b


def used_reasources(citys_reacources):
    a = []
    for n in citys_reacources:
        a.append(random.randint(0, n))

    return a


def USED_for_citys(citys_reacources):
    a = []
    for n in citys_reacources:
        a.append(random.randint(0, round(n * 1.3)))

    return a


def edit_colors(color, change):
    new_color = []
    multipy = 1
    for n in range(3):
        a = color[n] * change[n]
        if a > 250:
            x = 250 / a
            if x < multipy:
                multipy = x

        new_color.append(a)

    for n in range(3):
        new_color[n] = new_color[n] * multipy

    return new_color


def random_name():
    if random.randint(0, 1) == 0:
        a = BOY[random.randint(0, len(BOY) - 1)]
        c = BOY[random.randint(0, len(BOY) - 1)]
    else:
        a = GIRL[random.randint(0, len(GIRL) - 1)]
        c = GIRL[random.randint(0, len(GIRL) - 1)]

    b = LAST_NAMES[random.randint(0, len(LAST_NAMES) - 1)]

    if random.randint(1, 3) > 1 and not c == a:
        return a + " " + c + " " + b
    else:
        return a + " " + b


def scroll_line(surface, color, x, whole_length, surface_height, y, surface_start):
    if whole_length > 0:
        size = surface_height / (whole_length / surface_height)
        height = surface_start - (y / (whole_length / surface_height))

        if size < surface_height:
            pygame.draw.line(surface, color, (x, height),
                             (x, height + size), 6)


def mouse_in_rect(rect, bonus_pos=[0, 0]):
    mouse = pygame.mouse.get_pos()
    mouse = [mouse[0] - bonus_pos[0], mouse[1] - bonus_pos[1]]

    a = rect.topleft
    b = rect.bottomright
    if a[0] < mouse[0] and mouse[0] < b[0] and a[1] < mouse[1] and mouse[1] < b[1]:
        return True
    else:
        return False


def search_content(search, the_list):
    matching = [s for s in the_list if search in s]
    return matching


def change_surf_by_size(surface, wanted_size):
    if surface.get_size() != wanted_size:
        surface = pygame.Surface(wanted_size)


def textbox(surface, text, max_width, pos, font, color):
    a = text.split(" ")
    startx = pos[0]
    starty = pos[1]
    maximum = startx + max_width
    for n in a:
        pos[0] += 10
        b = font.render(n, True, color)
        
        assert max_width > b.get_width() + 10
        #always has to be true

        if pos[0] + b.get_width() > maximum:
            pos[0] = startx + 10
            pos[1] += 40
           
        surface.blit(b, pos)
        pos[0] += b.get_width()
    
    return [(pos[1] + b.get_height()) - starty, pos]

def fake_transparent(color1, color2, percent):
    a = []
    for n in range(3):
        a.append(max((min(color1[n], color2[n]) + (color1[n] - color2[n]) * min(percent, 1)), 0))
    return a

def every_ticks(gap):
    if pygame.time.get_ticks() % gap == 0:
        return True
    return False

BUTTON_NAMES = []
BUTTON_STATE = []

def check_released(button):
    if not BUTTON_NAMES.__contains__(button):
        BUTTON_NAMES.append(button)
        BUTTON_STATE.append(False)

    x = BUTTON_NAMES.index(button)

    if int(button) > 12:
        key = pygame.key.get_pressed()
        #if button.isdigit():
            #button = int(button)

        if key[button]:
            if not BUTTON_STATE[x]:
                BUTTON_STATE[x] = True
                return True
        else:
            BUTTON_STATE[x] = False
    else:
        button = button % 3
        hihi = pygame.mouse.get_pressed(3)[button]

        if hihi:
            if not BUTTON_STATE[x]:
                BUTTON_STATE[x] = True
                return True
        else:
            BUTTON_STATE[x] = False

    return False