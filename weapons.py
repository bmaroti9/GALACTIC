import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

with open("shoot_info.txt", "r") as f:
    INFO = json.load(f)

class Shot(pygame.sprite.Sprite):
    def __init__(self, pos, color, direction, appointed, speeds):
        super().__init__()
        info = INFO[str(color)]

        self.ages = info["ages"]
        self.last = self.ages[len(self.ages) - 1] - 1
        self.zoom = info["zoom"]

        self.appointed = appointed
        self.costumes = []
        for n in range(len(self.ages) - 1):
            a = pygame.image.load(
                "images/shoot_" + str(color) + str(n + 1) + ".png")
            self.costumes.append(a)

        self.angle = direction + 90

        self.y = math.sin(self.angle / 180.0 * math.pi) * 10 + speeds[1]
        self.x = math.cos(self.angle / 180.0 * math.pi) * 10 + speeds[0]

        self.pos = pos
        self.progress = 0

    def update(self, surface):
        self.progress += 1
        self.pos[0] += self.x
        self.pos[1] += self.y

        for n in range(len(self.ages) - 1):
            if self.progress > self.ages[n] and self.progress <= self.ages[n + 1]:
                self.image = self.costumes[n]

        screen_focus = get_screen_focus()
        
        self.real_x = screen_focus.pos[0] - self.pos[0] + surface.get_width() / 2
        self.real_y = screen_focus.pos[1] - self.pos[1] + surface.get_height() / 2

        self.image = pygame.transform.rotozoom(self.image, (-self.angle) + 180, self.zoom)
        self.rect = self.image.get_rect()
        self.rect.center = [self.real_x, self.real_y]

        surface.blit(self.image, self.rect)

        if self.progress > self.last:
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()

        self.speed = speed
        self.pos = [pos[0] - 10, pos[1] - 10]
        self.images = []
        for n in range(1, 3):
            a = pygame.image.load("images/bomb" + str(n) + ".png")
            a = pygame.transform.rotozoom(a, 0, 0.2)
            self.images.append(a)

        print(self.images)

        self.flash_speed = 40
        self.pause = 10
    
    def update(self, surface, spaceships):
        self.pause += 1
        if self.pause == 10:
            self.flash_speed = self.flash_speed // 2
            self.pause = 0

            if self.flash_speed == 10:
                self.boom(spaceships)
                self.flash_speed = 10
        
        print("flash_speed", self.flash_speed)

        if every_ticks(self.flash_speed // 4):
            print("reverse", len(self.images))
            self.images.reverse()
            print("this is what it looks like", len(self.images))
        
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.speed[0] = self.speed[0] * 0.96
        self.speed[1] = self.speed[1] * 0.96
        surface.blit(self.images[0], self.pos)
        
    def boom(self, spaceships):
        self.kill()


BOMBS = pygame.sprite.Group()
SHOTS = pygame.sprite.Group()

def add_bomb(pos, speed):
    BOMBS.add(Bomb(pos, speed))

def update_bombs(surface, spaceships):
    for n in BOMBS:
        n.update(surface, spaceships)

def add_shot(pos, color, direction, appointed, speeds):
    SHOTS.add(Shot(pos, color, direction, appointed, speeds))


def test_shots(sprite):
    return pygame.sprite.spritecollideany(sprite, SHOTS)

def kill_shots():
    SHOTS.empty()
    print(SHOTS)


def update_shots(surface):
    for shot in SHOTS:
        shot.update(surface)
