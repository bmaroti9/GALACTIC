import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time
import json

from weapons import *
from player import *
from opponent import *
from star import *
from map_mode import *
from sun import *
from fight_mode import *
from reasources import *
from person import *
from spaceships import *
from Joystick import *
from network_helper import *
from screen_shake import *
from people import *

# pygame.init()
SCORE_FONT = pygame.font.SysFont("Verdana", 16)
MUSIC_FONT = pygame.font.SysFont("comicsansms", 13)
LABEL_FONT = pygame.font.SysFont('simsun', 15)
#JOYSTICK = Joystick()

def game_over(surface, CLOCK, SUN, STARS, sound1):
    time.sleep(0.2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        surface.fill((30, 30, 45))

        for star in STARS:
            star.update(surface, [0, 0])

        font = pygame.font.SysFont('microsoftnewtailue', 120)
        wrighting = font.render(
            "GAME OVER!", True, ((250, 70, 0)))
        rect = wrighting.get_rect()
        rect.center = [surface.get_width() // 2,
                       surface.get_height() // 2 - 100]

        font2 = pygame.font.SysFont('microsoftnewtailue', 60)

        restart = button(surface, "RESTART", font2, (250, 150, 0),
                         (50, 150, 50), [surface.get_width() // 2,
                         surface.get_height() // 2 - 30, 1], -1, (254, 200, 50))

        main = button(surface, "QUIT TO MAIN MENU", font2, (250, 150, 0),
                      (50, 150, 50), [surface.get_width() // 2,
                      surface.get_height() // 2 + 40, 1], -1, (254, 200, 50))

        if restart:
            return game(surface, CLOCK, sound1, False)
        elif main:
            return start_menu(surface, CLOCK, sound1)

        surface.blit(wrighting, rect)

        pygame.display.update()
        CLOCK.tick(20)


def start_menu(surface, CLOCK, sound1):
    time.sleep(0.2)
    font = pygame.font.SysFont('microsoftnewtailue', 70)
    STARS = []
    x = round((surface.get_height() * surface.get_width()) // 3000)
    for _ in range(x):
        STARS.append(Star(surface.get_width(), surface.get_height()))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        surface.fill((30, 30, 45))

        for star in STARS:
            star.update(surface, [0, 0])

        logo = pygame.image.load(
            "images/GALACTIC_logo.png").convert_alpha()
        rect = logo.get_rect()
        rect.center = [surface.get_width() // 2,
                       surface.get_height() // 2 - 130]

        surface.blit(logo, rect)

        a = button(surface, "START NEW", font, (250, 150, 0),
                   (0, 0, 0), [surface.get_width() // 2,
                               surface.get_height() // 2 - 30, 1], -1, (254, 200, 50))

        b = button(surface, "RESUME SAVED", font, (100, 70, 0),
                   (250, 150, 0), [surface.get_width() // 2,
                                   surface.get_height() // 2 + 50, 1], -1, (100, 70, 0))

        c = button(surface, "QUIT", font, (250, 150, 0),
                   (250, 150, 0), [surface.get_width() // 2,
                                   surface.get_height() // 2 + 130, 1], -1, (254, 200, 50))

        if a:
            return game(surface, CLOCK, sound1, False)
        if b and False:
            return game(surface, CLOCK, sound1, True)
        if c:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        CLOCK.tick(20)
    
    send_kill_me()


def game(surface, CLOCK, sound1, load):
    time.sleep(0.2)
    
    kill_all_mine()
    
    PERSON = Person(surface)
    
    SUN = Sun()
    PLANETS = pygame.sprite.Group()
    for _ in range(8):
        PLANETS.add(Planet(SUN, PLANETS, surface))

    SCORE = 0
    STARS = []
    x = round((surface.get_height() * surface.get_width()) // 3000)
    for _ in range(x):
        STARS.append(Star(surface.get_width(), surface.get_height()))

    add_to_my_spaceships(Spaceship(random.randint(3, 3), personal_name(), [4000, 4000]))
    for _ in range(10):
        name = random_name()
        add_to_my_spaceships(Spaceship(3, name, 
            [random.randint(-4500, -4500), random.randint(-4500, -4500)]))
        add_bot(name, SUN, PLANETS)

    set_focus(get_my_spacehip())

    kill_shots()

    #if load:
        #loading(PLAYER, OPPONENTS, PLANETS, SUN)

    for n in PLANETS:
        n.after_loading(surface, load)

    THRUST = pygame.mixer.Sound("Sounds/engine-sound.wav")
    THRUST.play(-1)
    THRUST.set_volume(0)
    sound1.set_volume(0.1)

    SHAKES = pygame.Surface([surface.get_width(), surface.get_height()])
    offset = repeat((0, 0))

    screen_f = get_screen_focus()
    #buttons = JOYSTICK.get_button()

    while True:
        scroll = 1
        big_event = pygame.event.get()
        for event in big_event:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0 or event.key == pygame.K_v:
                    screen_f.mode = -screen_f.mode
                elif event.key == pygame.K_s and False:
                    save(screen_f, OPPONENTS, PLANETS, SUN)
                elif event.key == pygame.K_ESCAPE:
                    return start_menu(surface, CLOCK, sound1)
                elif pygame.key.get_mods() == 2:
                    reverse_view_mode()
                elif event.key == pygame.K_t:
                    set_focus(random.choice(get_spaceships()))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll = 1.12
                elif event.button == 5:
                    scroll = 0.88

        # print(pygame.key.get_mods())
        surface.fill((0, 0, 0))
        SHAKES.fill((0, 0, 0))

        if screen_f.mode == 1:
            fight_mode(SHAKES, STARS,
                       THRUST, SUN, [SCORE_FONT, MUSIC_FONT], PLANETS, PERSON)
        elif screen_f.mode == -1:
            map_mode(SHAKES, LABEL_FONT, screen_f, SUN, scroll, PLANETS)
        else:
            #land_mode(SHAKES, STARS, PLANETS,
                      #OPPONENTS, SUN, FR, screen_f, PERSON, scroll, big_event)
            pass
        
        update_other_spaceships()
        update_my_spaceships()

        volume = get_volume()
        if volume > 1: 
            offset = shake(volume, max(volume // 4, 2), min(volume // 2, 30))
            #offset = shake(volume, 6, 2)
        surface.blit(SHAKES, next(offset))

        #if PLAYER.is_dead():
            #sound1.set_volume(0)
            #THRUST.stop()
            #return game_over(surface, CLOCK, SUN, STARS, sound1)

        # print(len(OPPONENTS))
        pygame.display.update()
        CLOCK.tick(30)
        # print(CLOCK.get_rawtime())


def save(player, opponents, planets, sun):
    opponent_list = []

    for n in opponents:
        x = [n.pos, n.x_speed, n.y_speed, n.dead, n.angle]
        opponent_list.append(x)

    planet_list = []

    for n in planets:
        citys = []

        for b in n.citys:
            q = [b.name, b.city_type, b.angle]
            citys.append(q)

        x = [n.pos, n.color, n.name, n.size,
             n.city2, n.available_reasources, citys]
        planet_list.append(x)

    data = {"player": [player.spaceship, player.direction,
                       player.x_speed, player.y_speed, player.dead,
                       player.pos, player.score, player.resources],
            "opponents": opponent_list,
            "planets": planet_list,
            "sun": sun.name}

    with open("saves.txt", "w") as f:
        json.dump(data, f, indent=2)


def loading(player, opponents, planets, sun):
    with open("saves.txt", "r") as f:
        data = json.load(f)

    a = []

    player.spaceship = data["player"][0]
    player.direction = data["player"][1]
    player.x_speed = data["player"][2]
    player.y_speed = data["player"][3]
    player.dead = data["player"][4]
    player.pos = data["player"][5]
    player.score = data["player"][6]
    player.resources = data["player"][7]

    sun.name = data["sun"]

    index = 0
    for n in opponents:
        n.pos = data["opponents"][index][0]
        n.x_speed = data["opponents"][index][1]
        n.y_speed = data["opponents"][index][2]
        n.dead = data["opponents"][index][3]
        n.angle = data["opponents"][index][4]
        index += 1

    index = 0
    for n in planets:
        n.pos = data["planets"][index][0]
        n.color = data["planets"][index][1]
        n.name = data["planets"][index][2]
        n.size = data["planets"][index][3]
        n.city2 = data["planets"][index][4]
        n.available_reasources = data["planets"][index][5]
        n.citys = []
        for q in range(len(data["planets"][index][6])):
            n.citys.append(City(data["planets"][index]
                           [4], data["planets"][index][5]))
            n.citys[len(n.citys) - 1].name = data["planets"][index][6][q][0]
            n.citys[len(n.citys) - 1].city_type = data["planets"][index][6][q][1]
            n.citys[len(n.citys) - 1].angle = data["planets"][index][6][q][2]

        index += 1
