import pygame
from random import randint
from itertools import repeat

def shake(strength, times, speed):
    s = -1
    for _ in range(0, times):
        for x in range(0, strength, speed):
            yield (x*s, 0)
        for x in range(strength, 0, speed):
            yield (x*s, 0)
        s *= -1
    while True:
        yield (0, 0)

def main():
    pygame.init()
    org_screen = pygame.display.set_mode((400, 400))
    screen = org_screen.copy()
    screen_rect = screen.get_rect()
    player = pygame.Rect(180, 180, 20, 20)

    def get_rock():
        return pygame.Rect(randint(0, 340), 0, 60, 60)

    falling = get_rock()
    clock = pygame.time.Clock()

    # 'offset' will be our generator that produces the offset
    # in the beginning, we start with a generator that 
    # yields (0, 0) forever
    offset = repeat((0, 0))

    # this function creates our shake-generator
    # it "moves" the screen to the left and right
    # three times by yielding (-5, 0), (-10, 0),
    # ... (-20, 0), (-15, 0) ... (20, 0) three times,
    # then keeps yieling (0, 0)

    while True:
        if pygame.event.get(pygame.QUIT): break
        pygame.event.pump()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.move_ip(0, -2)
        if keys[pygame.K_a]: player.move_ip(-2, 0)
        if keys[pygame.K_s]: player.move_ip(0, 2)
        if keys[pygame.K_d]: player.move_ip(2, 0)
        player.clamp_ip(screen_rect) 

        falling.move_ip(0, 4)
        org_screen.fill((0, 0, 0))
        screen.fill((255,255,255))
        pygame.draw.rect(screen, (0,0,0), player)
        pygame.draw.rect(screen, (255,0,0), falling)

        if player.colliderect(falling):
            # if the player is hit by the rock,
            # we create a new shake-generator
            offset = shake(6, 8, 6)
            falling = get_rock()

        if not screen_rect.contains(falling):
            falling = get_rock()

        clock.tick(100)
        # here we draw our temporary surface to the
        # screen using the offsets created by the 
        # generators.
        org_screen.blit(screen, next(offset))
        pygame.display.flip()

if __name__ == '__main__':
    main()