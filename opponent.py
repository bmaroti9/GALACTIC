import math
import pygame
from pygame.locals import *
import random

from helpers import *
from shots import *
from reasources import *

with open("ships.txt", "r") as f:
    DATA = json.load(f)


class Opponent(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        self.spaceship = random.randint(0, 5)
        self.info = DATA[self.spaceship]

        self.sound2 = pygame.mixer.Sound("Sounds/shoot_special.wav")
        self.kaboom = pygame.mixer.Sound("Sounds/kaboom.wav")

        self.flameless = pygame.image.load(
            "images/" + str(self.info["name"]) + ".png").convert_alpha()
        self.flameless = pygame.transform.rotozoom(
            self.flameless, 0.0, self.info["shrink"])

        self.flames = []
        for n in [1, 2, 3, 4]:
            image = pygame.image.load(
                "images/" + str(self.info["name"]) + str(n) + ".png")
            image = pygame.transform.rotozoom(
                image, 0.0, self.info["shrink"]).convert_alpha()
            self.flames.append(image)

        self.rect = self.flameless.get_rect()

        self.want_to_attack = []

        self.pos = [player.pos[0] + random.randint(-5000, 5000),
                    player.pos[1] + random.randint(-5000, 5000)]
        self.x_speed = 0
        self.y_speed = 0
        self.angle = 0
        self.real_x = 1000
        self.real_y = 1000
        self.turning = 0
        self.dead = 0
        self.c = False
        self.dead_costumes = []
        self.target = 0
        self.gun_timer = 0
        self.thrust = 1
        self.unaccurate = 0
        for n in range(9):
            a = pygame.image.load(
                "images/explosion" + str(n + 1) + ".png")
            self.dead_costumes.append(a)

    def fighting(self, surface, player, opponents, arrow, FR):
        if random.randint(0, 60) == 1:
            self.new_target(player, opponents)

        angle = (self.target - self.angle) % 360
        you_can_shoot = 0

        if angle < 180:
            self.turning += 0.6
        elif angle > 180:
            self.turning -= 0.6

        if angle > 340 or angle < 20:
            you_can_shoot = 1
        
        if random.randint(1, 2) != 2 and self.gun_timer == 0:
            self.gun_timer = self.gun_timer = 50

        self.angle += self.turning
        self.turning = self.turning * 0.92

        self.real_x = player.pos[0] - self.pos[0] + surface.get_width() / 2
        self.real_y = player.pos[1] - self.pos[1] + surface.get_height() / 2

        self.c = self.real_x > -100 and self.real_x < surface.get_width() + 100 and \
            self.real_y > -100 and self.real_y < surface.get_height() + 100

        self.f = abs(360 - angle) < 80

        if self.gun_timer == 0 and self.dead == 0 and self.c and self.f and you_can_shoot == 1:

            speeds = (player.x_speed - self.x_speed,
                      player.y_speed - self.y_speed)

            for n in self.info["guns"]:
                hihi = rotating_position(n[0], n[1], self.angle,
                                         (self.real_x, self.real_y))
                add_shot(Shot(hihi, -self.angle, self,
                              speeds))
                self.gun_timer = 50
            
            if len(self.info["guns"]) > 0:
                self.sound2.stop()
                self.sound2.play()
                self.sound2.set_volume(0.2)

        if self.gun_timer > 0:
            self.gun_timer -= 1

        self.pos[0] += self.x_speed
        self.pos[1] += self.y_speed

        
        j = 1000 / (distance(self.pos, player.pos) + 0.00000001)
        if self.dead > 0:
            index = 0
            for n in self.dead_costumes:
                if self.dead > index and self.dead <= index + 3:
                    self.to_draw = n
                index += 3
            self.dead += 1
            huhu = 0
            
            self.kaboom.play()
            if j < 0.1:
                self.kaboom.set_volume(j)
            else:
                self.kaboom.set_volume(0.1)

            if self.dead > 26:
                colors = [(50, 200, 50), (250, 250, 50),
                          (250, 50, 50), (160, 99, 159)]
                for n in range(4):
                    geptuke = random.randint(-150, 100)
                    if geptuke > 0:
                        FR.add(floating_resource(
                            colors[n], geptuke, self.pos, n, [self.x_speed, self.y_speed]))

                if arrow.chosen == self:
                    arrow.chosen = 0
                self.kill()
                # print("killed")

        elif self.thrust == 1:
            self.x_speed += math.sin(self.angle / 180.0 * math.pi) * self.info["engine_efficiancy"]
            self.y_speed += math.cos(self.angle / 180.0 * math.pi) * self.info["engine_efficiancy"]
            self.to_draw = self.flames[random.randint(0, 3)]
            huhu = 1300 / (distance(self.pos, player.pos) + 0.00000001)
        else:
            self.to_draw = self.flameless
            huhu = 0

        if j < 0.13 and self.dead == 0:
            self.dead = 1
            print("to far")
        
        if random.randint(0, 1000) == 1:
            print(distance(self.pos, player.pos) + 0.00000001)


        if self.c:
            self.image = pygame.transform.rotate(self.to_draw, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = (self.real_x, self.real_y)

            surface.blit(self.image, self.rect)

        return huhu

    def new_target(self, player, opponents):
        everybody = self.get_list_of_in_range(player, opponents)

        if random.randint(0, 100) == 1:
            self.unaccurate = random.randint(-120, 120)

        if len(everybody) > 0:
            best = math.inf
            best_angle = 0
            for n in everybody:
                x = (self.x_speed - n.x_speed) ** 3
                y = (self.y_speed - n.y_speed) ** 3
                x += (self.pos[0] - n.pos[0]) * 0.32
                y += (self.pos[1] - n.pos[1]) * 0.32

                angle = calculate_angle([0, 0], [x, y]) + 180
                speed = math.sqrt((x ** 2) + (y ** 2))

                if speed < best:
                    # print(n)
                    best = speed
                    best_angle = angle

            self.target = (best_angle + self.unaccurate) % 360
            if best > 100:
                self.thrust = 1
            else:
                self.thrust = 0

    def get_list_of_in_range(self, player, opponents):
        everybody = [player]
        for n in opponents:
            everybody.append(n)

        a = []
        for n in everybody:
            x = distance(n.pos, self.pos)
            if x < random.randint(2500, 2500 * 1.5) and not n == self:
                a.append(n)

        return a
