import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

class Shot(pygame.sprite.Sprite):
    def __init__(self, pos, direction, appointed, speeds):
        super().__init__()

        self.appointed = appointed
        self.costumes = []
        for n in range(8):
            a = pygame.image.load(
                "images/shoot" + str(n + 1) + ".png")
            self.costumes.append(a)

        self.angle = direction - 90

        self.y = math.sin(self.angle / 180.0 * math.pi) * 10 + speeds[1]
        self.x = math.cos(self.angle / 180.0 * math.pi) * 10 + speeds[0]

        self.pos = pos
        self.progress = 0
        self.ages = [0, 3, 5, 7, 26, 28, 30, 32, 34]

    def update(self, surface):
        self.progress += 1
        self.pos[0] += self.x
        self.pos[1] += self.y

        for n in range(8):
            if self.progress > self.ages[n] and self.progress <= self.ages[n + 1]:
                self.image = self.costumes[n]

        self.image = pygame.transform.rotozoom(self.image, -self.angle, 0.4)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        surface.blit(self.image, self.rect)

        if self.progress > 32:
            self.kill()


SHOTS = pygame.sprite.Group()


def add_shot(shot):
    SHOTS.add(shot)


def test_shots(sprite):
    return pygame.sprite.spritecollideany(sprite, SHOTS)

def kill_shots():
    SHOTS.empty()
    print(SHOTS)


def update_shots(surface):
    for shot in SHOTS:
        shot.update(surface)
