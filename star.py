import math
import pygame
import random

from helpers import *


class Star(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.pos = [random.randint(0, screen_width),
                    random.randint(0, screen_height)]
        self.distance = random.randint(0, 100) * 0.002
        self.flash = random.randint(1, 8)
        self.a = random.randint(150, 250)

    def update(self, surface, player_speed):
        if self.pos[0] < -20 or self.pos[0] > surface.get_width() + 20:
            self.pos[0] = (surface.get_width() / 2 - self.pos[0]
                           ) + surface.get_width() / 2
        
        if self.pos[1] < -20 or self.pos[1] > surface.get_height() + 20:
            self.pos[1] = ((surface.get_height() / 2) - self.pos[1]) + \
                surface.get_height() / 2


        self.pos[0] += player_speed[0] * self.distance
        self.pos[1] += player_speed[1] * self.distance

        if random.randint(0, self.flash) == 5:
            self.a = random.randint(100, 250)

        # pygame.draw.circle(surface, (self.a, self.a, self.a), intpos(self.pos), 1)
        pygame.draw.rect(surface, (self.a, self.a, self.a), (intpos(self.pos), (2, 2)))

class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.red = pygame.image.load(
            "images/red_arrow.png").convert_alpha()
        self.green = pygame.image.load(
            "images/green_arrow.png").convert_alpha()
        self.chosen = 0

    def update(self, surface, player, SCORE_FONT):
        if isinstance(self.chosen, pygame.sprite.Sprite):
            dis = distance((player.pos[0], player.pos[1]), self.chosen.pos)
            if dis > 440:
                angle = calculate_angle(
                    [player.pos[0], player.pos[1]], self.chosen.pos)
                pos = rotating_position(
                    0, 150, angle, [surface.get_width() / 2, surface.get_height() / 2])
                self.copy = pygame.transform.rotozoom(
                    self.red, angle + 90, 0.15)
                self.rect = self.copy.get_rect()
                self.rect.center = (pos)
                surface.blit(self.copy, self.rect)

                dis = dis / 10

                if dis < 560:
                    hihi = SCORE_FONT.render(
                        "{:.2f}".format(dis) + "m", True, ((200, 200, 200)))
                else:
                    hihi = SCORE_FONT.render(
                        str(round(dis / 100) / 10) + "km", True, ((200, 200, 200)))

                rect = hihi.get_rect()
                rect.center = [pos[0], pos[1] + 20]
                surface.blit(hihi, rect)

    def backwards(self, direction, surface):
        pos = rotating_position(
            0, 150, direction, [surface.get_width() / 2, surface.get_height() / 2])
        self.copy = pygame.transform.rotozoom(self.green, direction + 90, 0.15)
        self.rect = self.copy.get_rect()
        self.rect.center = (pos)
        surface.blit(self.copy, self.rect)
