import math
import random
import sys
import os
import pygame
from pygame.locals import *
import time
import json

from localnet import *

with open("ships.txt", "r") as f:
    NETWORK = json.load(f)

def blank_networking():
    a = {
        "personal_code": random.randint(0, 99999)
    }
    return a

def personal_code():
    return NETWORK["personal_code"]

def recive_data():
    a = receive()
    return a

def list_of_all_ships(data):
    a = []
    for n in data:
        if data[0] == 'ship':
            ship = data[1]
            P_code = ship[0]
            pos = ship[1]
            direction = ship[2]
            image = ship[3]

def send_data(player):
    {
        "P_code": personal_code(),
        "pos": player
    }

    