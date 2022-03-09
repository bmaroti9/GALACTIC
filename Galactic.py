import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

from menus import *
from helpers import *

if 1 == 1:
    SCREEN_WIDTH = pygame.display.Info().current_w
    SCREEN_HEIGHT = pygame.display.Info().current_h - 50
else:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 660

print("init")
pygame.init()

SCORE_FONT = pygame.font.SysFont("Verdana", 16)
LOAD_FONT = pygame.font.SysFont("nanumsquareround", 40)
OPTIONS_FONT = pygame.font.SysFont("comicsansms", 35)
LABEL_FONT = pygame.font.SysFont("nanumsquareround", 13)
MUSIC_FONT = pygame.font.SysFont("comicsansms", 13)
CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("GALACTIC ©2021-2022 Dragon tail")

sound1 = pygame.mixer.Sound("Sounds/STAR_KNIGHT.wav")
sound1.play(-1)
sound1.set_volume(0.1)

SURFACE.fill((200, 200, 200))
image = pygame.image.load(
    "images/dragon_tail_plain_black.png").convert_alpha()
image = pygame.transform.rotozoom(image, 0, 0.3)
rect = image.get_rect()
rect.center = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
SURFACE.blit(image, rect)
pygame.display.update()
time.sleep(1)

print(pygame.font.get_fonts())

# image = pygame.image.load(
# "images/olga_rajza.png").convert_alpha()
#image = pygame.transform.rotozoom(image, 0, 0.55)
#rect = image.get_rect()
#rect.topleft = [0, 0]
#SURFACE.blit(image, rect)

# hihi = LOAD_FONT.render(
# "©2021 Dragon tail      V: 0.7", True, ((200, 0, 0)))
#hihi = pygame.transform.rotate(hihi, - 90)
#SURFACE.blit(hihi, (900, 50))
# pygame.display.update()
# time.sleep(1)hf   


start_menu(SURFACE, CLOCK, sound1)
