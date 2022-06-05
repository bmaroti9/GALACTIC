import math
import pygame
from pygame.locals import *
import random
import json

from helpers import *
from weapons import *
from reasources import *
from sun import *
from person import *
from star import *

with open("ships.txt", "r") as f:
    DATA = json.load(f)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, spaceship, owners_name, pos):
        super().__init__()

        self.wehicle_code = random.randint(0, 9999999999)
        self.sound = pygame.mixer.Sound("Sounds/engine-sound.wav")
        self.sound.play(-1)
        self.sound.set_volume(0)
        self.sound2 = pygame.mixer.Sound("Sounds/shoot_special.wav")
        self.kaboom = pygame.mixer.Sound("Sounds/kaboom.wav")
        self.spaceship = spaceship
        self.owners_name = owners_name
        self.angle = 0
        self.turning = 0
        self.x_speed = 0
        self.y_speed = 0
        self.gun_timer = 0
        self.dead = 0
        self.dead_costumes = []
        self.pos = pos
        self.resources = [40, 100, 40, 0]
        self.info = DATA[self.spaceship]
        self.correct_drift = [0, 0]
        self.correct_rotating_drift = 0
        self.controll = [0, 0, 0, 0]

        screen_focus = get_screen_focus()
        
        self.real_x = screen_focus.pos[0] - self.pos[0] + 1000
        self.real_y = screen_focus.pos[1] - self.pos[1] + 1000
    
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
    
    def update(self, surface):
        screen_focus = get_screen_focus()
        
        self.real_x = screen_focus.pos[0] - self.pos[0] + surface.get_width() / 2
        self.real_y = screen_focus.pos[1] - self.pos[1] + surface.get_height() / 2

        self.c = self.real_x > -100 and self.real_x < surface.get_width() + 100 and \
            self.real_y > -100 and self.real_y < surface.get_height() + 100

        if self.controll[1]:
            self.turning -= self.info["turning"] * 1.4
        if self.controll[2]:
            self.turning += self.info["turning"] * 1.4

        if self.controll[3] and self.gun_timer == 0:
            speeds = (screen_focus.x_speed - self.x_speed,
                      screen_focus.y_speed - self.y_speed)

            for n in self.info["guns"]:
                hihi = rotating_position(n[0], n[1], self.angle,
                                         (self.real_x, self.real_y))
                add_shot(hihi, "orange", -self.angle, self, speeds)
                self.gun_timer = self.info['gun_timer']
            
            if len(self.info["guns"]) > 0:
                self.sound2.stop()
                self.sound2.play()
                add_volume((400 - get_distance_from_focus(self.pos)) / 20)
                self.sound2.set_volume(0.2)
        
        #if self.controll[3] == 2:
            #print("almost")
            #if every_ticks(5):
                #add_bomb([self.real_x, self.real_y], [self.x_speed, self.y_speed])
        
        if self.gun_timer > 0:
            self.gun_timer -= 1
        
        self.pos[0] += self.x_speed + self.correct_drift[0]
        self.pos[1] += self.y_speed + self.correct_drift[1]

        self.angle += self.turning + self.correct_rotating_drift
        self.turning = self.turning * 0.92

        j = 1000 / (distance(self.pos, screen_focus.pos) + 0.00000001)
        if self.dead > 0:
            if self.dead == 4:
                add_volume((400 - get_distance_from_focus(self.pos)) / 5)
            
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
                        add_reasource(colors[n], geptuke, self.pos, n, [self.x_speed, self.y_speed])

                killed_chosen_maybe(self)
                self.kill()
    
        elif self.controll[0]:
            #increase = ((self.info["max_speed"] - (distance([0, 0], [self.x_speed, 
                    #self.y_speed]))) / (rev_percent(self.info["acceleration"], 20) * 10))

            self.x_speed += math.sin(self.angle / 180.0 * math.pi) * self.info["engine_efficiancy"]
            self.y_speed += math.cos(self.angle / 180.0 * math.pi) * self.info["engine_efficiancy"]
            self.to_draw = self.flames[random.randint(0, 3)]
            if random.randint(0, 3) == 0 and self.gun_timer < 16:
                add_volume((400 - get_distance_from_focus(self.pos)) / 80)
        else:
            self.to_draw = self.flameless

        self.image = pygame.transform.rotate(self.to_draw, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.real_x, self.real_y)

        if self.c:
            surface.blit(self.image, self.rect)
    
    def feed_input(self, inputs):
        self.controll = inputs
