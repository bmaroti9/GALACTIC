import math
import random
import sys
from helpers import *
import pygame
from pygame.locals import *
import time

pygame.init()

FONT1 = pygame.font.SysFont('microsoftnewtailue', 60)
FONT2 = pygame.font.SysFont("dejavuserif", 17)
FONT3 = pygame.font.SysFont('microsoftnewtailue', 30)
FONT4 = pygame.font.SysFont("ubuntu", 26)
FONT5 = pygame.font.SysFont('poorrichard', 30)


def People(Info, surface, city, PLANET, scroll, big_event):
    pos = Info.people_scroll
    screen_end = Info.people_surf.get_width()
    room = (surface.get_height() - pos - 20) // 40

    pygame.draw.rect(surface, PLANET.color, ((320, 128), (550, 35)), 2)

    if pygame.mouse.get_pressed(3)[0]:
        Info.people_search = mouse_in_rect(Rect(320, 128, 550, 35))

    if Info.people_search:

        hihi = FONT3.render(Info.people_word, True, (100, 100, 100))
        rect = hihi.get_rect()
        rect.midleft = (330, 144)
        surface.blit(hihi, rect)
        a = rect.topright[0]

        for event in big_event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(Info.people_word)

                elif event.key == pygame.K_BACKSPACE:
                    Info.people_word = Info.people_word[:-1]
                elif a < 850:
                    Info.people_word += event.unicode

        if pygame.time.get_ticks() % 1400 > 700:
            pygame.draw.line(surface, edit_colors(
                PLANET.color, (1.7, 1.7, 1.7)), (a, 133), (a, 158), 2)

    else:
        blit_text(surface, "Search", FONT5, (100, 100, 100), (360, 144), 2)
        Info.people_word = ""

    Info.people_surf.fill((0, 0, 0))

    huhu = search_content(Info.people_word, city.people)

    Info.people_scroll += (scroll - 1) * 400

    x = 0 - (len(huhu) * 40) + 460
    x = min(x, Info.people_surf.get_height() - 460)

    print(Info.people_scroll, x)

    if Info.people_scroll > -1:
        Info.people_scroll = 0
    elif Info.people_scroll < x:
        Info.people_scroll = x

    for n in huhu:

        button(Info.people_surf, n, FONT4,
               (150, 150, 150), (0, 0, 0), [30, pos, 0], -1, PLANET.color, [250, 180])

        button(Info.people_surf, "talk", FONT5, (100, 100, 200),
               (0, 0, 0), [400, pos, 0], -1, (200, 0, 0), [250, 180])

        pygame.draw.line(Info.people_surf, (80, 80, 80),
                         (0, pos + 33), (screen_end - 15, pos + 33), 2)
        pos += 40

    surface.blit(Info.people_surf, (250, 180))
    scroll_line(surface, PLANET.color, surface.get_width() -
                20, len(huhu) * 40, Info.people_surf.get_height(), Info.people_scroll, 180)

    # pygame.draw.rect(surface, PLANET.color, ((250, 180), people_surf.get_size()), 1)


def talk(surface, Info, city, PLANET, big_event):
    pos = Rect(335, surface.get_height() - 15 -
               Info.talk_word_y, 500, Info.talk_word_y)
    pygame.draw.rect(surface, PLANET.color, pos, 2)

    if pygame.mouse.get_pressed(3)[0]:
        Info.talk_search = mouse_in_rect(pos)

    y = 30

    if Info.talk_search:
        for event in big_event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and Info.talk_word != "":
                    q = textbox(surface, Info.talk_word,
                                480, [-1000, -1000], FONT3, PLANET.color)[0]

                    Info.talk_chat.insert(0, [Info.talk_word, q, 6, 0])
                    Info.talk_chat.insert(0, [Info.talk_word, q, 6, 1])
                    Find_response(Info.talk_word)
                    print(Info.talk_chat)
                    Info.talk_word = ""
                elif event.key == pygame.K_BACKSPACE:
                    Info.talk_word = Info.talk_word[:-1]
                else:
                    Info.talk_word += event.unicode

        a = textbox(surface, Info.talk_word, 480, [340,
                                                   surface.get_height() - 15 - Info.talk_word_y],
                    FONT3, (150, 150, 150))

        if pygame.time.get_ticks() % 1400 > 700:
            pygame.draw.line(surface, edit_colors(
                PLANET.color, (1.7, 1.7, 1.7)), (a[1][0], a[1][1] + 4), (a[1][0], a[1][1] + 36), 2)

        Info.talk_word_y = a[0]
        y += a[0]

    else:
        blit_text(surface, "Talk", FONT5, (100, 100, 100),
                  (pos.midleft[0] + 20, pos.midleft[1]), 2)
        y += 40

    index = 0
    for n in Info.talk_chat:
        if n[2] > 0.005:
            n[2] -= 0.01
        else:
            del Info.talk_chat[index]

        if n[3] == 0:
            c = PLANET.color
        else:
            c = (150, 150, 150)
        pygame.draw.rect(surface, fake_transparent(c, (0, 0, 0), n[2]),
                         ((335, surface.get_height() - n[1] - y), (500, n[1])))

        textbox(surface, n[0], 480, [
                335, surface.get_height() - n[1] - y], FONT3, (0, 0, 0))
        index += 1
        y += n[1] + 20


def Find_response(sentence):
    with open("talking.txt", "r") as f:
        talking = json.load(f)

    last_letter = sentence[-1]

    if last_letter == "?":
        oportunity_list = talking["Question"]
    else:
        oportunity_list = talking["Other"]

    if (str(sentence) in oportunity_list):
        print("t")
    else:
        print("f", oportunity_list)
