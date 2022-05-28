import math
import pygame
from pygame.locals import *
import random
import json

from helpers import *
from shots import *
from reasources import *
from sun import *
from person import *
from network_helper import *
from Joystick import *

with open("ships.txt", "r") as f:
    DATA = json.load(f)

pygame.joystick.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.sound = pygame.mixer.Sound("Sounds/engine-sound.wav")
        self.sound.play(-1)
        self.sound.set_volume(0)
        self.sound2 = pygame.mixer.Sound("Sounds/shoot_special.wav")
        self.kaboom = pygame.mixer.Sound("Sounds/kaboom.wav")
        self.spaceship = random.randint(0, 5)
        self.direction = 0
        self.turning = 0
        self.x_speed = 0
        self.y_speed = 0
        self.mode = 1
        self.gun_timer = 0
        self.dead = 0
        self.dead_costumes = []
        self.pos = [-1000, -1000]
        self.score = 0
        self.resources = [40, 100, 40, 0]
        self.info = DATA[self.spaceship]
        self.land_chaned_pos = True
        self.landed = False
        self.timer = 0
        self.thrust_level = 0

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

        for n in range(9):
            a = pygame.image.load(
                "images/explosion" + str(n + 1) + ".png")
            self.dead_costumes.append(a)
        
        self.apperance = Spaceship(surface, self.spaceship)

    def update(self, surface, sun, FR, planets, PERSON):
        if every_ticks(5):
            #send_data(self)
            pass
        
        keys = pygame.key.get_pressed()

        self.apperance.update(surface, keys[pygame.K_UP], keys[pygame.K_RIGHT], keys[pygame.K_LEFT], 
                    pygame.K_SPACE)
        self.rect = self.apperance.rect
        
        '''
        if self.timer > 0:
            self.timer -= 1

        if self.mode == 1:
            self.fight(surface, sun, FR, planets, PERSON)
            self.land_chaned_pos = True
        elif self.mode == 0:
            self.on_planet(surface, sun, planets, PERSON)
            if self.land_chaned_pos:
                PERSON.pos = [self.pos[0], self.pos[1]]
                self.land_chaned_pos = False
        '''

    def fight(self, surface, sun, FR, planets, PERSON):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.turning -= self.info["turning"]
        if keys[pygame.K_LEFT]:
            self.turning += self.info["turning"]

        pressed = keys[pygame.K_SPACE] or pygame.key.get_mods() == 128
        if pressed and self.gun_timer == 0 and self.dead == 0 and self.resources[2] > 0:
            for n in self.info["guns"]:
                hihi = rotating_position(
                    n[0], n[1], self.direction, (surface.get_width() / 2, surface.get_height() / 2))
                add_shot(Shot(hihi, -self.direction, self, [0, 0]))
                self.gun_timer = self.info["gun_timer"]
                self.resources[2] -= 1

            if len(self.info["guns"]) > 0:
                self.sound2.stop()
                self.sound2.play()
                self.sound2.set_volume(0.2)

        if keys[pygame.K_b] and self.landed != False and self.timer < 1:
            self.mode = 0
            self.timer = 20
            print(self.landed.pos)
            PERSON.height = distance(self.landed.pos, self.pos)

        if self.gun_timer > 0:
            self.gun_timer -= 1

        self.direction += self.turning
        self.turning = self.turning * 0.92

        h = check_reasources(
            [surface.get_width() / 2, surface.get_height() / 2], FR)

        if not h == 0:
            self.resources[h.reasource] += h.amount
            h.kill()

        self.pos[0] += self.x_speed
        self.pos[1] += self.y_speed

        g = gravity(self, sun, planets)
        self.x_speed += g[0]
        self.y_speed += g[1]

        self.thrust_controll(surface)

        if self.dead > 0:
            index = 0
            self.to_draw = 0
            for n in self.dead_costumes:
                if self.dead > index and self.dead <= index + 3:
                    self.to_draw = n
                index += 3
            self.dead += 1
            self.kaboom.play()
            self.kaboom.set_volume(0.1)
        elif self.thrust_level > 0 and self.resources[1] > 0:
            self.to_draw = self.flames[random.randint(0, 3)]
            self.x_speed += math.sin(self.direction /
                                     180.0 * math.pi) * self.thrust_level
            self.y_speed += math.cos(self.direction /
                                     180.0 * math.pi) * self.thrust_level
            self.sound.set_volume(1)
            self.resources[1] -= self.thrust_level / 3
        else:
            self.to_draw = self.flameless
            self.sound.set_volume(0)

        if not self.to_draw == 0:
            self.image = pygame.transform.rotate(self.to_draw, self.direction)
            self.rect = self.image.get_rect()
            self.rect.center = (surface.get_width() / 2,
                                surface.get_height() / 2)
            surface.blit(self.image, self.rect)

        self.stuff(surface)

    def on_planet(self, surface, sun, planets, PERSON):
        g = gravity(self, sun, planets)
        self.real_x = PERSON.pos[0] - self.pos[0] + surface.get_width() / 2
        self.real_y = PERSON.pos[1] - self.pos[1] + surface.get_height() / 2

        keys = pygame.key.get_pressed()
        p = abs(self.real_x - (surface.get_width() / 2)) + \
            abs(self.real_y - (surface.get_height() / 2))
        if keys[pygame.K_b] and p < 20 and self.timer < 1 and self.dead == 0:
            self.mode = 1
            self.timer = 20

        self.x_speed += g[0]
        self.y_speed += g[1]
        self.image = pygame.transform.rotate(self.flameless, self.direction)

        if self.dead > 0:
            self.x_speed = 0
            self.y_speed = 0
            
            index = 0
            
            self.image = 0
            for n in self.dead_costumes:
                if self.dead > index and self.dead <= index + 3:
                    self.image = n
                index += 3
            self.dead += 1
            self.kaboom.play()
            self.kaboom.set_volume(0.1) 

        if self.image != 0:
            self.rect = self.image.get_rect()
            self.rect.center = (self.real_x, self.real_y)
            surface.blit(self.image, self.rect)

    def stuff(self, surface):
        if self.resources[0] > 0:
            self.resources[0] -= 0.005
        elif self.dead == 0:
            self.dead = 1

        multipy = 1
        for n in self.resources:
            if n > 245:
                x = 245 / n
                if x < multipy:
                    multipy = x

        text = ["FOOD: ", "FUEL: ", "AMMUNITION: ", "JEWELRIES: "]
        font = pygame.font.SysFont("dejavuserif", 15)
        colors = [(50, 200, 50), (250, 250, 50), (250, 50, 50), (160, 99, 159)]
        pos = [surface.get_width() - 270, surface.get_height() - 85]
        for n in range(4):
            haha = font.render(
                text[n] + "{:.0f}".format(self.resources[n]), True, colors[n])
            rect = haha.get_rect()
            rect.midright = [pos[0] - 20, pos[1] + n * 20]
            surface.blit(haha, rect)
            pygame.draw.line(surface, colors[n], [
                             pos[0], pos[1] + n * 20],
                             [pos[0] + self.resources[n] * multipy, pos[1] + n * 20], 10)

    def thrust_controll(self, surface):
        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            self.thrust_level = self.info["engine_efficiancy"]
        else:
            self.thrust_level = 0

        pygame.draw.line(surface, (200, 200, 0), (40, surface.get_height() - 50),
                         (40 + (self.thrust_level * 4000), surface.get_height() - 50), 15)

    def is_dead(self):
        if self.mode == 0:
            return self.dead > 50 and self.landed == False
        elif self.mode == 1:    
            return self.dead > 50

#JOYSTICK = Joystick()
def controll_spaceship():
    #axes = JOYSTICK.get_axes()
    #buttons = JOYSTICK.get_button()
    #print(buttons)
    
    keys = pygame.key.get_pressed()
    inputs = [keys[pygame.K_UP], keys[pygame.K_RIGHT], keys[pygame.K_LEFT], keys[pygame.K_SPACE]]

    #inputs = [round(axes[1]) == -1, round(axes[0]) == 1, round(axes[0]) == -1, buttons[1]]

    return inputs


