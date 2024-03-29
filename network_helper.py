import math
import random
import sys
import os
import pygame
from pygame.locals import *
import time
import json

from localnet import *
from helpers import *
from spaceships import *
from people import *

with open("networking.txt", "r") as f:
    NETWORK = json.load(f)

def blank_networking():
    a = {
        "personal_name": random_name()
    }
    return a

def personal_name():
    return NETWORK["personal_name"]

def recive_data():
    a = receive()
    final = []

    for n in a:
        for hihi in n:
            final.append(hihi)
    
    return [final]

def send_my_data(my_spaceships):
    a = []
    if every_ticks(8):
        for n in my_spaceships:
            a.append(detailed_data(n))
    else:
        for n in my_spaceships:
            a.append(passby_data(n))
    #print("S", a)
    send(a)

def send_kill_me():
    a = {
        "kill" : personal_name()
    }
    return a
        
def return_kind_of_message(a):
    if "spaceship" in a:
        return "d"
    elif "kill" in a:
        return "k"
    else:
        return "p"

def detailed_data(spaceship):
    a = {
        "owners_name": spaceship.owners_name,
        "pos": [round(spaceship.pos[0]), round(spaceship.pos[1])],
        "angle": round(spaceship.angle),
        "speed": [float("{:.3f}".format(spaceship.x_speed)), float("{:.3f}".format(spaceship.y_speed))],
        "spaceship": spaceship.spaceship
    }
    return a

def passby_data(spaceship):
    a = {
        "owners_name": spaceship.owners_name,
        "inputs": spaceship.controll
    }
    return a


MY_SPACESHIPS = pygame.sprite.Group()
OTHER_SPACESHIPS = pygame.sprite.Group()

def update_other_spaceships():
    hihi = recive_data()
    #print("R", hihi)
    for n in hihi:
        #print("list_of_recived_from_only_one_other", n)
        for x in n:
            #print("P", x)
            kind = return_kind_of_message(x)
            if kind == "d":
                #print("SHOULD HAVE ADDED 1111111111111111111111111111111111111111111111")
                spaceship_check(x)
            elif kind == "p":
                passby_update(x)
            elif kind == "k":
                kill_one_player(x["kill"])

def update_my_spaceships():
    for n in MY_SPACESHIPS:
        if n.owners_name == personal_name():
            keys = pygame.key.get_pressed()
            inputs = [keys[pygame.K_UP], keys[pygame.K_RIGHT], keys[pygame.K_LEFT], keys[pygame.K_SPACE]]
            n.feed_input(inputs)
        else:
            inputs = get_bot_controll(n, get_spaceships())
            n.feed_input(inputs)
    
    send_my_data(MY_SPACESHIPS)

def spaceship_check(detailed_data):
    global MY_SPACESHIPS
    global OTHER_SPACESHIPS
    
    all_names = [i.owners_name for i in get_spaceships()]
    other_names = [i.owners_name for i in OTHER_SPACESHIPS]

    #print("N", detailed_data)
    name_of_new = detailed_data["owners_name"]
    if other_names.__contains__(name_of_new):
        already_existing = OTHER_SPACESHIPS.sprites()[other_names.index(name_of_new)]
        drift_x = detailed_data["pos"][0] - already_existing.pos[0]
        drift_y = detailed_data["pos"][1] - already_existing.pos[1]
        drift_angle = detailed_data["angle"] - already_existing.angle
        already_existing.correct_drift = [drift_x / 8, drift_y / 8]
        already_existing.correct_rotating_drift = drift_angle / 8
        already_existing.x_speed = detailed_data["speed"][0]
        already_existing.y_speed = detailed_data["speed"][1]
    elif not all_names.__contains__(name_of_new):
        #print("THIS SHOULD NOT HAVE HAPPENED!", detailed_data)
        new_spacehip = Spaceship(detailed_data["spaceship"], detailed_data["owners_name"], 
                detailed_data["pos"])
        OTHER_SPACESHIPS.add(new_spacehip)
        

def passby_update(passby_data):
    global MY_SPACESHIPS
    global OTHER_SPACESHIPS
    
    other_names = [i.owners_name for i in OTHER_SPACESHIPS]

    #print("Pudzi makes sure", passby_data)
    name_of_new = passby_data["owners_name"]
    if other_names.__contains__(name_of_new):
        spaceship = OTHER_SPACESHIPS.sprites()[other_names.index(name_of_new)]
        spaceship.feed_input(passby_data["inputs"])

def get_spaceships():
    spaceships = []

    for n in MY_SPACESHIPS:
        spaceships.append(n)
    for n in OTHER_SPACESHIPS:
        spaceships.append(n)
    
    return spaceships

def add_to_my_spaceships(item):
    global MY_SPACESHIPS

    MY_SPACESHIPS.add(item)

def kill_one_player(personal_name):
    spaceships = get_spaceships()
    
    other_names = [i.owners_name for i in spaceships]
    already_existing = spaceships.sprites()[other_names.index(personal_name)]
    already_existing.kill()

def get_my_spacehip():
    names = [i.owners_name for i in MY_SPACESHIPS]
    index = names.index(personal_name())
    return MY_SPACESHIPS.sprites()[index]

def kill_all_mine():
    for n in MY_SPACESHIPS:
        n.kill()

