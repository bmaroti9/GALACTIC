import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

INDUSTRY_TEXT = ["FOOD:  ", "FUEL:  ", "AMMUNITION:  ", "JEWELRIES:  "]
INDUSTRY_COLORS = [(50, 200, 50), (250, 250, 50),
                   (250, 50, 50), (200, 99, 200)]

pygame.init()

FONT1 = pygame.font.SysFont("latinmodernmonolight", 60)
FONT2 = pygame.font.SysFont("dejavuserif", 17)
FONT3 = pygame.font.SysFont("latinmodernmonolight", 30)
FONT4 = pygame.font.SysFont("ubuntu", 26)
FONT5 = pygame.font.SysFont("latinmodernmonoslanted", 30)


def Industies(surface, city, colored, gray, first):
    multipy = (surface.get_width() - 650) / 100
    if first:
        q = gray
    else:
        q = colored

    hihi = surface.get_width() - 650

    for n in q:
        if n * multipy > hihi:
            x = hihi / n
            if x < multipy:
                multipy = x

    pos = [600, 170]
    for n in range(4):
        blit_text(surface, INDUSTRY_TEXT[n], FONT2, INDUSTRY_COLORS[n], [
            pos[0] - 320, (pos[1] - 10) + n * 30], 0)

        if first:
            text = "{:.0f}".format(
                colored[n]) + " / " + "{:.0f}".format(gray[n])
        else:
            text = "{:.0f}".format(
                gray[n]) + " / " + "{:.0f}".format(colored[n])

        blit_text(surface, text, FONT2, INDUSTRY_COLORS[n], [
            pos[0] - 30, (pos[1] - 10) + n * 30], 3)

        if gray[n] * multipy > 2 and first:
            pygame.draw.line(surface, (150, 150, 150), [
                pos[0], pos[1] + n * 30], [pos[0] + gray[n] * multipy, pos[1] + n * 30], 16)

        if colored[n] * multipy > 2:
            pygame.draw.line(surface, INDUSTRY_COLORS[n], [
                pos[0], pos[1] + n * 30], [pos[0] + colored[n] * multipy, pos[1] + n * 30], 16)

            if first:
                a = pos[0] + colored[n] * multipy
            else:
                a = pos[0] + gray[n] * multipy

            pygame.draw.line(surface, edit_colors(INDUSTRY_COLORS[n], (0.5, 0.5, 0.5)),
                             [a, pos[1] + n * 30 - 7], [
                a, pos[1] + n * 30 + 8], 3)

        if gray[n] * multipy - 2 > 2 and not first:
            pygame.draw.line(surface, (150, 150, 150), [
                pos[0], pos[1] + n * 30], [pos[0] + gray[n] * multipy - 2, pos[1] + n * 30], 16)