
import math
import pygame
import random


class Planet:
    def __init__(self, world_pos_x: float, world_pos_y: float, radius: float):
        self.world_pos_x = world_pos_x
        self.world_pos_y = world_pos_y
        self.radius = radius
        self.color = (random.randint(0, 255),
                      random.randint(0, 255),
                      random.randint(0, 255))

    def update(self, world: 'World'):
        screen_pos_x = self.world_pos_x - world.world_view_x
        screen_pos_y = self.world_pos_y - world.world_view_y

        pygame.draw.circle(world.surface, self.color,
                           (screen_pos_x, screen_pos_y), self.radius)


class Ship():
    def __init__(self, world_pos_x: float, world_pos_y: float):
        self.normal_image = pygame.image.load(
            "images/Lemming.png").convert_alpha()
        self.normal_image = pygame.transform.rotozoom(
            self.normal_image, -90, 0.25)

        self.thrust_image = pygame.image.load(
            "images/Lemming1.png").convert_alpha()
        self.thrust_image = pygame.transform.rotozoom(
            self.thrust_image, -90, 0.25)

        self.world_pos_x = world_pos_x
        self.world_pos_y = world_pos_y
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.angle = 200.0
        self.thrusting = True

    def update_position(self, world: 'World'):
        if self.thrusting:
            accel_x = math.cos(self.angle / 180 * math.pi)
            accel_y = math.sin(self.angle / 180 * math.pi)

            power = 0.2
            self.speed_x += accel_x * power
            self.speed_y -= accel_y * power

            # limit speed
            max_speed = 20
            speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
            if speed > max_speed:
                self.speed_x = self.speed_x / speed * max_speed
                self.speed_y = self.speed_y / speed * max_speed

        self.world_pos_x += self.speed_x
        self.world_pos_y += self.speed_y

        # limit distance from center
        max_dist = 2 * world.world_radius
        dist = math.sqrt(self.world_pos_x ** 2 + self.world_pos_y ** 2)
        if dist > max_dist:
            self.world_pos_x = self.world_pos_x / dist * max_dist
            self.world_pos_y = self.world_pos_y / dist * max_dist

    def update(self, world: 'World'):
        self.update_position(world)

        screen_pos_x = self.world_pos_x - world.world_view_x
        screen_pos_y = self.world_pos_y - world.world_view_y

        image = self.thrust_image if self.thrusting else self.normal_image
        image = pygame.transform.rotate(image, self.angle)
        rect = image.get_rect()
        rect.center = (screen_pos_x, screen_pos_y)

        world.surface.blit(image, rect)


class World:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MALACTIC")

        self.surface = pygame.display.set_mode((2000, 1600))
        self.screen_width = self.surface.get_width()
        self.screen_height = self.surface.get_height()
        self.clock = pygame.time.Clock()

        self.world_radius = 0.5 * max(self.screen_width, self.screen_height)
        self.world_view_x = - self.screen_width / 2
        self.world_view_y = - self.screen_height / 2

        self.create_planets(10)
        self.ship = Ship(0, 0)

    def create_planets(self, count: int):
        self.planets = []
        while len(self.planets) < count:
            radius = random.randint(50, 300)
            pos_x = random.randint(-self.world_radius, self.world_radius)
            pos_y = random.randint(-self.world_radius, self.world_radius)

            overlap = False
            for planet in self.planets:
                dist = math.sqrt((planet.world_pos_x - pos_x) ** 2 +
                                 (planet.world_pos_y - pos_y) ** 2)
                if dist <= radius + planet.radius + 100:
                    overlap = True

            if not overlap:
                self.planets.append(Planet(pos_x, pos_y, radius))

    def run(self):
        while True:
            self.surface.fill((200, 200, 200))

            for planet in self.planets:
                planet.update(self)
            self.ship.update(self)

            pygame.display.update()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            self.ship.thrusting = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.ship.angle = math.fmod(self.ship.angle + 5, 360)
            if keys[pygame.K_RIGHT]:
                self.ship.angle = math.fmod(self.ship.angle - 5, 360)
            if keys[pygame.K_UP]:
                self.ship.thrusting = True

            # see more in the direction we are going
            self.world_view_x = self.ship.world_pos_x - self.screen_width / 2 + \
                20 * self.ship.speed_x
            self.world_view_y = self.ship.world_pos_y - self.screen_height / 2 + \
                20 * self.ship.speed_y


if __name__ == '__main__':
    world = World()
    world.run()
